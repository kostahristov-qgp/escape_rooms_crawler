#!/bin/bash

# Ensure the list file exists
if [[ ! -f websites_list.txt ]]; then
    echo "websites_list.txt not found!"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Get the current date for the log file name
log_file="logs/$(date +%F).log"

# Loop over each line in the list
while IFS= read -r name; do
    script="${name}.py"
    if [[ -f "$script" ]]; then
        echo "🚀 Running $script..." | tee -a "$log_file"
        python "$script" 2>&1 | tee -a "$log_file"
        echo "✅ Finished $script" | tee -a "$log_file"
        echo "⏳ Sleeping 30 seconds before next crawler..." | tee -a "$log_file"
        sleep 30
    else
        echo "❌ Skipped $script (not found)" | tee -a "$log_file"
    fi
done < websites_list.txt