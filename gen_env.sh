#!/bin/bash -e

# 加入 .env.common* (如果存在) 到環境變數檔案清單
env_files=$(ls .env.common* 2>/dev/null | sort | xargs)

# 根據傳入參數，決定要加入的環境變數檔案
for arg in "$@"; do
	f=$arg
	# 當傳入的參數不是檔案時，改為查看 .env.* 檔案
	[[ ! -f $f ]] && f=".env.$arg"
	[[ -f $f ]] && {
		# 將符合條件的檔案加入合併列表
		env_files="${env_files} ${f}"
	} || {
		# 若都不存在則印出提示
		printf "\e[38;5;208m""Not found: {'$arg', '.env.$arg'}\n""\e[0m"
	}
done

# 若沒有任何檔案被合併，則印出提示
[[ -z $env_files ]] && {
	printf "\e[38;5;196m""No env files merged!\n""\e[0m"
	exit 1
}

# 開始合併檔案內容
printf "\e[38;5;245m""Merging: $env_files\n""\e[0m"
contents="# ( merge from: ${env_files} )"
for f in ${env_files}; do
	contents="${contents}\n\n# ( from: ${f} )\n\n$(grep . ${f} || :)"
done

# 備份 .env 檔案
[[ -f .env ]] && {
	printf "\e[38;5;208m""Backup: .env -> .env.bak\n""\e[0m"
	mv .env .env.bak
}

# 將合併結果寫入 .env 檔案
printf "%b\n" "${contents}" >".env"
printf "\e[32m""Merged to: .env\n""\e[0m"
