#!/bin/bash
# --------------------------------------------
# schedule_stop.sh
# --------------------------------------------

export RESULTS_DIR="${RESULTS_DIR:-/root/Results}"

DEFAULT_DELAY_MINUTES=30
DELAY_MINUTES=${1:-$DEFAULT_DELAY_MINUTES}

STOP_JOB_FILE="/tmp/stopexperiment.pid"
LOG_FILE="$RESULTS_DIR/experiment_schedule.log"

timestamp() {
    date +"[%Y-%m-%d %H:%M:%S]"
}

oeo_log() {
    log_to_oeo.py "$1" "$2"
}

# Cancel old job
if [ -f "$STOP_JOB_FILE" ]; then
    OLD_PID=$(cat "$STOP_JOB_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        kill "$OLD_PID"
    fi
    rm -f "$STOP_JOB_FILE"
fi

# Schedule new stop
DELAY_SECONDS=$((DELAY_MINUTES * 60))

(
    sleep "$DELAY_SECONDS"
    echo "$(timestamp) Experiment stopped after $DELAY_MINUTES minutes." | tee -a "$LOG_FILE"
    oeo_log INFO "Experiment stopped after $DELAY_MINUTES minutes" > /dev/null 2>&1
    /root/stopexperiment.sh
) &

NEW_PID=$!
echo "$NEW_PID" > "$STOP_JOB_FILE"
echo "$(timestamp) Experiment is scheduled to stop in $DELAY_MINUTES minutes." | tee -a "$LOG_FILE"
oeo_log INFO "Experiment is scheduled to stop in $DELAY_MINUTES minutes" > /dev/null 2>&1

