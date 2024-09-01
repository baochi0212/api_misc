rm -rf ./all_valid_key
count_file=0
file_name=$1
echo "File name $file_name"
max_parallel=`wc -l $file_name`  # Adjust based on your system resources

for key in $(cat $1); do
    echo "Processing $count_file"

    (  # Subshell for iioutput handling and backgrounding
      output=$(python test_api.py $key | head)
      echo $output

      if [[ $output == "Fail" ]]; then
        echo "Invalid $count_file"
      else
        echo "Valid key $count_file"
        echo $key >> all_valid_key
      fi

    ) &  # Run the subshell in the background

    let count_file=count_file+1

    # Control parallelism
    num_running=$((num_running + 1))
    if [[ $num_running == $max_parallel ]]; then
      wait
      num_running=$((num_running - 1))
    fi
  done

  wait  # Wait for any remaining processes to finish
