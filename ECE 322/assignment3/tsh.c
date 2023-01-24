/*
 * tsh - A tiny shell program with job control
 *
 * jyollesmurph -- Jonah 'jay' Yolles-Murphy
 * jboesen -- John Boesen
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <inttypes.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <assert.h>
#include <stdbool.h>

#define SCOPE_TRACE_ENABLED 1

#pragma GCC diagnostic error "-Wall"
#pragma GCC diagnostic error "-Wunused-result"

// required for the SCOPE_DEBUG utility
#pragma GCC diagnostic ignored "-Wunused-variable"

/* Misc manifest constants */
#define MAXLINE 1024             /* max line size */
#define MAXARGS 128              /* max args on a command line */
#define MAXJOBS 16               /* max jobs at any point in time */
#define MAXJID  ((jid_t)1 << 16) /* max job ID */

// /* Job states */
/*
 * Jobs states: FG (foreground), BG (background), ST (stopped)
 * Job state transitions and enabling actions:
 *     FG -> ST  : ctrl-z
 *     ST -> FG  : fg command
 *     ST -> BG  : bg command
 *     BG -> FG  : fg command
 * At most 1 job can be in the FG state.
 */
typedef enum {
    JOB_UNDEF = 0,
    JOB_FOREGND = 1,
    JOB_BACKGND = 2,
    JOB_STOPPED = 3,

    UNDEF = JOB_UNDEF,
    FG = JOB_FOREGND,
    BG = JOB_BACKGND,
    ST = JOB_STOPPED,
} job_state_t;

const char *const job_state_name[] = {
    "UNDEF",
    "FOREGND",
    "BACKGND",
    "STOPPED"};

typedef int jid_t;

typedef char **mut_argv_t;

typedef const char *const *const_argv_t;

typedef struct job {              /* The job struct */
    pid_t       pid;              /* job PID */
    jid_t       jid;              /* job ID [1, 2, ...] */
    job_state_t state;            /* UNDEF, BG, FG, or ST */
    char        cmdline[MAXLINE]; /* command line */
} job_t;

/* Global variables */
extern char **environ;            /* defined in libc */
char          prompt[] = "tsh> "; /* (DO NOT CHANGE) command line prompt  */
size_t prompt_length = 4; /* (DO NOT CHANGE) the length of the prompt */

bool verbose = false;       /* if true, print additional output */
bool scope_trace = false;   /* if true, the scope traces will be printed*/
static jid_t nextjid = 1;   /* next job ID to allocate */
static char  sbuf[MAXLINE]; /* for composing sprintf messages */

job_t  jobs[MAXJOBS] = {0}; /* The job list */
size_t n_jobs = 0;
pid_t  parent_pid = {0};

/* End global variables */

/* ========== [ utils ] ========== */

/**
 * @brief A sugar-only macro used to enforce for loop structure
 *
 * @param name the name of the loop variable
 * @param start <int> the first number to emit when iterating
 * @param upto <int> stop iterating when reached, excluded from emitted
 * values
 * @param step <int> the value to jump by between iterations
 */
#define range(name, start, upto, step)          \
    int name = start;                           \
    (step > 0) ? (name < upto) : (name > upto); \
    name += step

/**
 * @brief Terminal escape color codes
 */
#define ESC_BLK "\e[30m"
#define ESC_RED "\e[31m"
#define ESC_GRN "\e[32m"
#define ESC_YLW "\e[33m"
#define ESC_BLU "\e[34m"
#define ESC_MAG "\e[35m"
#define ESC_CYN "\e[36m"
#define ESC_WHT "\e[37m"
#define ESC_RST "\e[0m"

/**
 * @brief prints only if there verbose is on
 *
 */
#define printf_verbose(...)               \
    if (verbose) {                        \
        printf(ESC_CYN ":%i", getpid());  \
        printf(": " ESC_RST __VA_ARGS__); \
    }

/**
 * @brief Prints a message of including the funciton name and related data on
 * the entrance and exit of the scope (the current block`{...}`) this macro
 * is called in to the top of a function body
 */
#if SCOPE_TRACE_ENABLED == 1
#    define SCOPE_TRACE()                                           \
        const char *const _scope_debug##__COUNTER__                 \
            __attribute__((__cleanup__(_print_scope_exit_debug))) = \
                _print_scope_enter_debug(__func__)
#else
SCOPE_TRACE()
#endif
const char *const _print_scope_enter_debug(const char *const name);
void              _print_scope_exit_debug(const char *const *const name);

/* ========== [ function prototypes and related constants ] ========== */

void eval(const char *const cmdline);
void __attribute__((noreturn)) cleanup_exit(int status);

bool do_if_builtin_cmd(const char *const cmdline, mut_argv_t argv);
void start_new_job(
    const char *const cmdline,
    mut_argv_t        argv,
    bool              is_backgnd);

typedef enum {  // Info from Child Status
    SIGCODE_NOOP = 0,
    SIGCODE_EXITED = CLD_EXITED,
    SIGCODE_KILLED = CLD_KILLED,
    SIGCODE_DUMPED = CLD_DUMPED,
    SIGCODE_TRAPPED = CLD_TRAPPED,
    SIGCODE_STOPPED = CLD_STOPPED,
    SIGCODE_CONTINUED = CLD_CONTINUED,
} siginfo_code_t;

const char *const siginfo_code_name[] = {
    "NOOP",
    "EXITED",
    "KILLED",
    "DUMPED",
    "TRAPPED",
    "STOPPED",
    "CONTINUED"};

// helpers for managing jobs
void  waitfg(pid_t pid);
pid_t Fork(void);

// signal related

/**
 * @brief applys a full sigmask for the duration of the scope (the current
 * `{}` block) this macro is called in
 *
 */
#define SCOPE_SIG_BLOCK_ALL()                    \
    const sigset_t _scope_sig_block##__COUNTER__ \
        __attribute__((__cleanup__(sig_restore))) = sig_block_all()

sigset_t get_current_sigset(void);
int      sigset_as_int(sigset_t mask);
sigset_t sig_block_all();
void     sig_restore(const sigset_t *const prev);

void sigchld_handler(int sig);
void sigtstp_handler(int sig);
void sigint_handler(int sig);

// builtin commands and related functions
void builtin_bgfg_callback(mut_argv_t argv);
void builtin_jobs_callback(mut_argv_t argv);
void builtin_quit_callback(mut_argv_t argv);
void builtin_echo_callback(mut_argv_t argv);

void do_bg_fg(pid_t pid, bool is_backgnd);

struct {
    const char *const name;
    void (*func)(mut_argv_t);
} builtin_cmd_set[] = {
    // Execute the correct builtin function
    {"bg", &builtin_bgfg_callback},
    {"fg", &builtin_bgfg_callback},
    {"jobs", &builtin_jobs_callback},
    {"quit", &builtin_quit_callback},
    {"echo",
     &builtin_echo_callback}  // no this is not "builtin" but it is useful
                              // and we don't have $PATH implemented
};

const size_t n_builtin_commands =
    sizeof(builtin_cmd_set) / sizeof(builtin_cmd_set[0]);

/* ========== [ provided function prototypes ] ========== */
/* Here are helper routines that we've provided for you */
job_state_t parseline(const char *cmdline, char **argv);
void        sigquit_handler(int sig);

void  clearjob(job_t *job);
void  initjobs(job_t *jobs);
jid_t maxjid(job_t *jobs);
int   addjob(
      job_t            *jobs,
      pid_t             pid,
      job_state_t       state,
      const char *const cmdline);
bool   deletejob(job_t *jobs, pid_t pid);
pid_t  fgpid(job_t *jobs);
job_t *getjobpid(job_t *jobs, pid_t pid);
job_t *getjobjid(job_t *jobs, jid_t jid);
jid_t  pid2jid(pid_t pid);
void   listjobs(job_t *jobs);

void         print_usage(void);
void         unix_error(char *msg);
void         app_error(char *msg);
typedef void handler_t(int);
handler_t   *Signal(int signum, handler_t *handler);

/* ========== [ function implementations ] ========== */

/*
 * main - The shell's main routine
 */
int main(int argc, char **argv) {
    char c;
    char cmdline[MAXLINE];
    bool emit_prompt = true; /* emit prompt (default) */
    parent_pid = getpid();

    /* Redirect stderr to stdout (so that driver will get all output
     * on the pipe connected to stdout) */
    dup2(1, 2);

    /* Parse the command line */
    while ((c = getopt(argc, argv, "hvps")) != EOF) {
        switch (c) {
            case 'h': /* print help message */
                print_usage();
                break;
            case 'v': /* emit additional diagnostic info */
                verbose = true;
                break;
            case 's': /* emit additional diagnostic info */
                scope_trace = true;
                break;
            case 'p':                /* don't print a prompt */
                emit_prompt = false; /* handy for automated testing */
                break;
            default:
                print_usage();
        }
    }

    /* Install the signal handlers */

    /* These are the ones you will need to implement */
    Signal(SIGINT, sigint_handler);   /* ctrl-c */
    Signal(SIGTSTP, sigtstp_handler); /* ctrl-z */
    Signal(SIGCHLD, sigchld_handler); /* Terminated or stopped child */

    /* This one provides a clean way to kill the shell */
    Signal(SIGQUIT, sigquit_handler);

    /* Initialize the job list */
    initjobs(jobs);

    /* Execute the shell's read/eval loop */
    while (1) {
        /* Read command line */
        if (emit_prompt) {
            printf("%s", prompt);
            fflush(stdout);
        }
        if ((fgets(cmdline, MAXLINE, stdin) == NULL) && ferror(stdin))
            app_error("fgets error");
        if (feof(stdin)) { /* End of file (ctrl-d) */
            fflush(stdout);
            cleanup_exit(0);
        }

        /* Evaluate the command line */
        eval(cmdline);
        fflush(stdout);
        fflush(stdout);
    }

    cleanup_exit(0); /* control never reaches here */
}

/*
 * eval - Evaluate the command line that the user has just typed in
 *
 * If the user has requested a built-in command (quit, jobs, bg or fg)
 * then execute it immediately. Otherwise, fork a child process and
 * run the job in the context of the child. If the job is running in
 * the foreground, wait for it to terminate and then return.  Note:
 * each child process must have a unique process group ID so that our
 * background children don't receive SIGINT (SIGTSTP) from the kernel
 * when we type ctrl-c (ctrl-z) at the keyboard.
 */
void eval(const char *const cmdline) {
    // SCOPE_TRACE();

    char       *argv[MAXLINE] = {NULL};
    job_state_t bg_state = parseline(cmdline, argv);
    if (!argv[1] &&
        !strcmp(
            argv[0],
            "bg")) {  // Check to see if there is no PID passed for bg or fg
        printf("bg command requires PID or %%jobid argument\n");
        return;
    }
    if (!argv[1] && !strcmp(argv[0], "fg")) {
        printf("fg command requires PID or %%jobid argument\n");
        return;
    }

    if (do_if_builtin_cmd(cmdline, argv))
        ;
    else
        start_new_job(cmdline, argv, bg_state == JOB_BACKGND);

    return;
}

void __attribute__((noreturn)) cleanup_exit(int status) {
    // for (range(idx, 0, MAXJOBS, 1)) {
    //     job_t *job = &jobs[idx];
    //     if (job->state != JOB_UNDEF) {
    //         kill(-job->pid, SIGTERM);
    //     }
    // }
    // printf("\n\n!!!!!!! EXIT %i \n\n, ", status);
    exit(status);
}

/**
 * @brief forks and starts a new process, returns the pid
 *
 * @param argv the arguemnts to pass to the program, the first entry in argv
 * must be the file to execute
 * @return pid_t
 */
pid_t execute_argv(mut_argv_t argv) {
    pid_t pid = 0;
    if ((pid = Fork()) == 0) {
        setpgid(0, 0);

        if (execve(argv[0], argv, environ) <
            0) {  // Execute child code and raise error if needed
            printf(
                "%s: Command not found. (some other error may have "
                "occured)\n",
                argv[0]);
            cleanup_exit(-1);
        }
        __builtin_unreachable();
        printf_verbose("THE F*CK IS HAPPENING IF THIS IS PRINTING\n");
    }
    return pid;
}

/**
 * @brief if the passed command is a buildin, execute the buildin command
 *
 * @param cmdline
 * @param argv
 * @return true if is is a builtin command and was executed
 * @return false if not a builtin, you should handle it otherwise
 */
bool do_if_builtin_cmd(const char *const cmdline, mut_argv_t argv) {
    // OPTIMIZE: only make one lowercase buffer once for the longest stretch

    // In this function we only use strn* library functions so we ignore the
    // null terminator

    // if it is a builtin, execute it
    for (range(idx, 0, n_builtin_commands, 1)) {
        const char *const builtin_name = builtin_cmd_set[idx].name;

        // make a lowercase version of the first n characters in the cmd line
        // so we can compare against it
        const size_t len = strlen(builtin_name);
        char         cmdline_buf[len];
        strncpy(cmdline_buf, cmdline, len);
        for (range(idx, 0, len, 1))
            cmdline_buf[idx] = tolower(cmdline_buf[idx]);

        // if the builtin command matches, run that functions
        if (0 == strncmp(cmdline_buf, builtin_name, len)) {
            printf_verbose(
                ESC_BLU "{builtin}" ESC_RST " '%s' command\n", builtin_name);
            builtin_cmd_set[idx].func(argv);
            return true;
        }
    }

    return false;
}

void start_new_job(
    const char *const cmdline,
    mut_argv_t        argv,
    bool              is_backgnd) {
    //
    SCOPE_TRACE();

    pid_t child_pid = execute_argv(argv);

    // Output for background process: [jid] (pid) cmdline
    addjob(
        jobs,
        child_pid,
        is_backgnd ? JOB_BACKGND : JOB_FOREGND,
        cmdline == NULL ? argv[0] : cmdline);
    job_t *job = getjobpid(jobs, child_pid);
    if (job == NULL) {
        unix_error("start_new_job");
    }

    printf_verbose(
        "Started pid:%i in %s cmd=%s\n",
        child_pid,
        is_backgnd ? "background" : "foreground",
        job->cmdline);

    do_bg_fg(child_pid, is_backgnd);
}

pid_t Fork(void) {
    SCOPE_SIG_BLOCK_ALL();

    pid_t pid;

    if ((pid = fork()) < 0) {
        unix_error("Fork error");
    }

    return pid;
}

sigset_t sig_block_all() {
    sigset_t mask;
    sigset_t prev;
    sigfillset(&mask);
    sigprocmask(SIG_SETMASK, &mask, &prev);

    return prev;
}

void sig_restore(const sigset_t *const prev) {
    // SCOPE_TRACE();
    sigprocmask(SIG_SETMASK, prev, NULL);
}

void builtin_echo_callback(mut_argv_t argv) {
    // this is cheating, don't do this. However,
    mut_argv_t mut_argv = (mut_argv_t)argv;
    mut_argv[0] = "/bin/echo";

    start_new_job(NULL, mut_argv, false);
};

/*
 * builtin_bgfg_callback - parse the argv for bf/fg commands then execute
 * theri functions
 */
void builtin_bgfg_callback(mut_argv_t argv) {
    SCOPE_TRACE();
    pid_t pid;

    // determine if bg or fg
    bool              is_backgnd = false;
    const char *const arg0 = argv[0];
    if (0 == strcmp(arg0, "bg"))  // determine whether we are sending process
                                  // to the foreground or background
        is_backgnd = true;
    else if (0 == strcmp(arg0, "fg"))
        is_backgnd = false;
    else
        app_error("(builtin_bgfg_callback) argv[0] not bg or fg");

    // extract the pid
    const char *const arg1 = argv[1];
    job_t            *job;
    if (arg1[0] == '%') {  // jid
        jid_t jid = strtoumax(&arg1[1], NULL, 10);
        job = getjobjid(jobs, jid);
        if (!job) {
            printf("%s: No Such Job\n", arg1);
            return;
        }
        pid = getjobjid(jobs, jid)->pid;
    } else if ('0' <= arg1[0] && arg1[0] <= '9') {  // pid
        pid = strtoumax(arg1, NULL, 10);
    } else {
        printf(
            "%s argument must be a PID or %%jobid\n",
            is_backgnd ? "bg" : "fg");
        return;
    }

    do_bg_fg(pid, is_backgnd);
}

/**
 * @brief for fg move a programt o the foreground and wait for it to end, for
 * bg send sigcont then display the realted information
 *
 * @param pid
 * @param is_backgnd
 */
void do_bg_fg(pid_t pid, bool is_backgnd) {
    job_t *job = getjobpid(jobs, pid);

    if (job == NULL) {
        printf("(%i): No such process\n", pid);
        return;
    }

    if (is_backgnd) {  // Change state and restart the process
        job->state = JOB_BACKGND;
        kill(-pid, SIGCONT);
        printf("[%d] (%d) %s\n", job->jid, pid, job->cmdline);

    } else {
        // move the process into the forground and wait for it to terminate
        job->state = JOB_FOREGND;
        kill(-pid, SIGCONT);
        // wait for it to terminate (ie foreground behavior)
        waitfg(pid);
    }

    return;
}

void builtin_jobs_callback(mut_argv_t argv) {
    listjobs(jobs);
    return;
}

__attribute__((noreturn)) void builtin_quit_callback(mut_argv_t argv) {
    // iterate thorugh all the children and send them sigquit

    cleanup_exit(0);
}

/*
 * waitfg - Block until process pid is no longer the foreground process
 */
void waitfg(pid_t pid) {
    // nice docs: https://linux.die.net/man/3/waitpid

    siginfo_t info = {0};

    int wait_err = waitid(P_PID, pid, &info, WEXITED | WSTOPPED | WNOWAIT);
    if (wait_err == -1) unix_error("(waitfg)");

    siginfo_code_t code = info.si_code;

    switch (code) {  // Print statement if child exited normally
        case SIGCODE_STOPPED:
        case SIGCODE_EXITED:
            printf_verbose(
                "Child %i terminated with exit code %i \n",
                pid,
                info.si_status);
            break;
        default:
            break;
    }
}

/*****************
 * Signal handlers
 *****************/

/*
 * sigchld_handler - The kernel sends a SIGCHLD to the shell whenever
 *     a child job terminates (becomes a zombie), or stops because it
 *     received a SIGSTOP or SIGTSTP signal. The handler reaps all
 *     available zombie children, but doesn't wait for any other
 *     currently running children to terminate.
 */
void sigchld_handler(int sig) {
    SCOPE_TRACE();
    SCOPE_SIG_BLOCK_ALL();

    // 0 = alive, -1 = error
    siginfo_t info = {0};

    pid_t wait_err = waitid(
        P_ALL, 0, &info, WEXITED | WSTOPPED | WCONTINUED /* | WNOWAIT */);

    if (wait_err != 0) unix_error("(sigchld_handler) cannot find process");

    pid_t pid = info.si_pid;

    job_t *job = getjobpid(jobs, pid);
    if (job == NULL) app_error("(sigchld_handler) no matching job for pid");

    printf_verbose(
        ESC_GRN "(sigchld_handler) " ESC_RST "Recieved %s state: %s ",
        siginfo_code_name[info.si_code],
        job_state_name[job->state]);

    switch (
        (siginfo_code_t)info
            .si_code) {  // Print and do action depending on child sigcode
        case SIGCODE_KILLED:
            printf("Job [%d] (%d) terminated by signal 2\n", job->jid, pid);
            deletejob(jobs, pid);
            break;
        case SIGCODE_EXITED:
            deletejob(jobs, pid);
            break;
        case SIGCODE_STOPPED:
            printf("Job [%d] (%d) Stopped by signal 20\n", job->jid, pid);
            job->state = JOB_STOPPED;
            break;

        case SIGCODE_CONTINUED:
            // do nothing
            break;

        default:
            unix_error("(sigchld_handler) not acounted for");
            break;
    }
}

/*
 * sigint_handler - The kernel sends a SIGINT to the shell whenver the
 *    user types ctrl-c at the keyboard.  Catch it and send it along
 *    to the foreground job.
 */
void sigint_handler(int sig) {
    SCOPE_TRACE();

    const int olderrno = errno;
    pid_t     job_pid = fgpid(jobs);

    if (job_pid > 0) {  // Send through the signal
        job_t *job = getjobpid(jobs, job_pid);
        kill(-job_pid, SIGINT);
    } else if (job_pid < 0) {
        unix_error("sigint_handler (pid kill)");
    }

    errno = olderrno;
    return;
}

/*
 * sigtstp_handler - The kernel sends a SIGTSTP to the shell whenever
 *     the user types ctrl-z at the keyboard. Catch it and suspend the
 *     foreground job by sending it a SIGTSTP.
 */
void sigtstp_handler(int sig) {
    SCOPE_TRACE();
    SCOPE_SIG_BLOCK_ALL();

    const int olderrno = errno;
    pid_t     jobpid = fgpid(jobs);

    printf_verbose(
        ESC_MAG "(sigtstp_handler)" ESC_RST "  fgpid=%i\n", jobpid);

    if (n_jobs == 0) {
        return;

    }

    else if (jobpid > 0) {  // Send through the signal
        job_t *job = getjobpid(jobs, jobpid);
        if (job == NULL) {
            unix_error("(sigstp_handler)");
        }
        kill(-jobpid, SIGSTOP);
    } else {
        unix_error("sigstp_handler");
    }

    if (verbose) {
        job_t *job = getjobpid(jobs, jobpid);
        printf_verbose(
            "check for pid: %i state:%s\n",
            jobpid,
            job_state_name[job->state]);
    }

    errno = olderrno;
    return;
}

/*
 * sigquit_handler - The driver program can gracefully terminate the
 *    child shell by sending it a SIGQUIT signal.
 */
void sigquit_handler(int sig) {
    printf("\nTerminating after receipt of SIGQUIT signal\n");
    cleanup_exit(1);
}

/*********************
 * End signal handlers
 *********************/

/* ========== [ provided functions ] =========== */

/*
 * parseline - Parse the command line and build the argv array.
 *
 * Characters enclosed in single quotes are treated as a single
 * argument.  Return JOB_BACKGND if the user has requested a BG job,
 * false if the user has requested a JOB_FOREGND job.
 */
job_state_t parseline(const char *const cmdline, char **argv) {
    static char array[MAXLINE]; /* holds local copy of command line */
    char       *buf = array;    /* ptr that traverses command line */
    char       *delim;          /* points to first space delimiter */
    int         argc;           /* number of args */
    int         bg;             /* background job? */

    strcpy(buf, cmdline);
    buf[strlen(buf) - 1] = ' ';   /* replace trailing '\n' with space */
    while (*buf && (*buf == ' ')) /* ignore leading spaces */
        buf++;

    /* Build the argv list */
    argc = 0;
    if (*buf == '\'') {
        buf++;
        delim = strchr(buf, '\'');
    } else {
        delim = strchr(buf, ' ');
    }

    while (delim) {
        argv[argc++] = buf;
        *delim = '\0';
        buf = delim + 1;
        while (*buf && (*buf == ' ')) /* ignore spaces */
            buf++;

        if (*buf == '\'') {
            buf++;
            delim = strchr(buf, '\'');
        } else {
            delim = strchr(buf, ' ');
        }
    }
    argv[argc] = NULL;

    if (argc == 0) /* ignore blank line */
        return 1;

    /* should the job run in the background? */
    if ((bg = (*argv[argc - 1] == '&')) != 0) {
        argv[--argc] = NULL;
    }

    return (bg) ? JOB_BACKGND : JOB_FOREGND;
}

/***********************************************
 * Helper routines that manipulate the job list
 **********************************************/

/* clearjob - Clear the entries in a job struct */
void clearjob(job_t *job) {
    job->pid = 0;
    job->jid = 0;
    job->state = JOB_UNDEF;
    job->cmdline[0] = '\0';
}

/* initjobs - Initialize the job list */
void initjobs(job_t *jobs) {
    int i;

    for (i = 0; i < MAXJOBS; i++) clearjob(&jobs[i]);
    n_jobs = 0;
}

/* maxjid - Returns largest allocated job ID */
jid_t maxjid(job_t *jobs) {
    int   i;
    jid_t max = 0;

    for (i = 0; i < MAXJOBS; i++)
        if (jobs[i].jid > max) max = jobs[i].jid;
    return max;
}

/* addjob - Add a job to the job list */
int addjob(
    job_t            *jobs,
    pid_t             pid,
    job_state_t       state,
    const char *const cmdline) {
    int i;

    if (pid < 1) return 0;

    for (i = 0; i < MAXJOBS; i++) {
        if (jobs[i].pid == 0) {
            jobs[i].pid = pid;
            jobs[i].state = state;
            jobs[i].jid = nextjid++;
            if (nextjid > MAXJOBS) nextjid = 1;
            strcpy(jobs[i].cmdline, cmdline);
            // remove the newline terminator
            jobs[i].cmdline[strlen(jobs[i].cmdline) - 1] = '\0';

            printf_verbose(
                "Added job [%d] %d cmd='%s'\n",
                jobs[i].jid,
                jobs[i].pid,
                jobs[i].cmdline);

            // cleanup and stracking
            n_jobs += 1;

            return 1;
        }
    }
    printf("Tried to create too many jobs\n");
    return 0;
}

/* deletejob - Delete a job whose PID=pid from the job list */
bool deletejob(job_t *jobs, pid_t pid) {
    int i;

    if (pid < 1) return false;
    // printf_verbose("PID of deleted job: %d\n", pid);
    for (i = 0; i < MAXJOBS; i++) {
        if (jobs[i].pid == pid) {
            clearjob(&jobs[i]);
            nextjid = maxjid(jobs) + 1;
            n_jobs -= 1;
            return true;
        }
    }
    return false;
}

/* fgpid - Return PID of current foreground job, 0 if no such job */
pid_t fgpid(job_t *jobs) {
    int i;

    for (i = 0; i < MAXJOBS; i++)
        if (jobs[i].state == JOB_FOREGND) return jobs[i].pid;
    return 0;
}

/* getjobpid  - Find a job (by PID) on the job list */
job_t *getjobpid(job_t *jobs, pid_t pid) {
    int i;

    if (pid < 1) return NULL;
    for (i = 0; i < MAXJOBS; i++) {
        if (jobs[i].pid == JOB_UNDEF) continue;
        if (jobs[i].pid == pid) return &jobs[i];
    }
    return NULL;
}

/* getjobjid  - Find a job (by JID) on the job list */
job_t *getjobjid(job_t *jobs, jid_t jid) {
    int i;

    if (jid < 1) return NULL;
    for (i = 0; i < MAXJOBS; i++)
        if (jobs[i].jid == jid) return &jobs[i];
    return NULL;
}

/* pid2jid - Map process ID to job ID */
jid_t pid2jid(pid_t pid) {
    int i;

    if (pid < 1) return 0;
    for (i = 0; i < MAXJOBS; i++)
        if (jobs[i].pid == pid) {
            return jobs[i].jid;
        }
    return 0;
}

/* listjobs - Print the job list */
void listjobs(job_t *jobs) {
    int i;

    for (i = 0; i < MAXJOBS; i++) {
        if (jobs[i].pid != 0) {
            printf("[%d] (%d) ", jobs[i].jid, jobs[i].pid);
            switch (jobs[i].state) {
                case JOB_BACKGND:
                    printf("Running");
                    break;
                case JOB_FOREGND:
                    printf("Foreground");
                    break;
                case JOB_STOPPED:
                    printf("Stopped");
                    break;
                default:
                    printf(
                        "listjobs: Internal error: job[%d].state=%d",
                        i,
                        jobs[i].state);
            }
            printf(" %s\n", jobs[i].cmdline);
        }
    }
}

/******************************
 * end job list helper routines
 ******************************/

/***********************
 * Other helper routines
 ***********************/

/*
 * usage - print a help message
 */
void print_usage(void) {
    printf("Usage: shell [-hvp]\n");
    printf("   -h   print this message\n");
    printf("   -v   print additional diagnostic information\n");
    printf(
        "   -s   print function enter/exit diagnostic information for "
        "specifically marked functions\n");
    printf("   -p   do not emit a command prompt\n");
    cleanup_exit(1);
}

/*
 * unix_error - unix-style error routine
 */
void unix_error(char *msg) {
    fprintf(stdout, "%s: %s\n", msg, strerror(errno));
    cleanup_exit(1);
}

/*
 * app_error - application-style error routine
 */
void app_error(char *msg) {
    fprintf(stdout, "%s\n", msg);
    cleanup_exit(1);
}

/*
 * Signal - wrapper for the sigaction function
 */
handler_t *Signal(int signum, handler_t *handler) {
    struct sigaction action, old_action;

    action.sa_handler = handler;
    sigemptyset(&action.sa_mask); /* block sigs of type being handled */
    action.sa_flags = SA_RESTART; /* restart syscalls if possible */

    if (sigaction(signum, &action, &old_action) < 0)
        unix_error("Signal error");
    return (old_action.sa_handler);
}

/* ========== [ custom debug related functions / utils ] ========== */
int _indent_level = 0;

const char *const _print_scope_enter_debug(const char *const name) {
    if (scope_trace) {
        size_t spaces_count = 4 * (_indent_level++);
        char  *spaces = alloca(spaces_count + 1);
        memset(spaces, ' ', spaces_count);
        spaces[spaces_count] = '\0';

        printf(
            (ESC_RED "\n%s[>pid:%i '%s' " ESC_RST "sigmask:%x scope \n"),
            spaces,
            getpid(),
            name,
            sigset_as_int(get_current_sigset()));
        return name;
    } else {
        return NULL;
    }
}

void _print_scope_exit_debug(const char *const *const name) {
    if (*name != NULL) {
        size_t spaces_count = 4 * (--_indent_level);
        char  *spaces = alloca(spaces_count + 1);
        memset(spaces, ' ', spaces_count);
        spaces[spaces_count] = '\0';

        // read current sigset

        printf(
            (ESC_RED "\n%s<]pid:%i '%s' " ESC_RST "sigmask:%x scope \n"),
            spaces,
            getpid(),
            *name,
            sigset_as_int(get_current_sigset()));
    }
}

int sigset_as_int(sigset_t mask) {
    union to_int {
        sigset_t sig;
        int      num;
    };

    union to_int asint = (union to_int){.sig = mask};

    return asint.num;
}

sigset_t get_current_sigset(void) {
    sigset_t mask;
    sigprocmask(SIG_SETMASK, NULL, &mask);
    return mask;
}
