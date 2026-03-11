eosls -l /store/user/xinlongl/XHY4bRun3_skim/*2022*QCD* | awk '{sum += $5} END {printf "%.2f GiB\n", sum/1024/1024/1024}'
