#!/bin/bash
#====================================================================
# Renting-STD Restart Script
# /bin/sh start_stop.sh 参数1 参数2
# 参数1：代表动作，start | stop | status | restart | check
# 参数2：代表启动几个进程，默认是1
#====================================================================
cmd_action=$1
process_num=$2
# 加载必要的环境变量
source /etc/profile

# 自定义常量
SERVICE_NAME="renting-std"
SERVICE_HOME="/usr/local/${SERVICE_NAME}"
JAR_NAME="manage_std.py"
LOG_PATH="/var/log/${SERVICE_NAME}.log"

# 日志打印函数
print_msg() {
    printf '%b\n' "【`date +%Y-%m-%d\ %H:%M:%S`】 $1" | tee -a $LOG_PATH
}

print_info() {
    print_msg "\33[34m${1} [♫]\33[0m"
}

print_success() {
    #print_msg "\33[32m${1}[✔]\33[0m"
    print_msg "\33[32m${1}【SUCCESS】\33[0m"
}

print_warning() {
    print_msg "\33[33m${1}【WARNING】\33[0m"
}

print_error() {
    #print_msg "\33[31m${1}[✘]\33[0m"
    print_msg "\33[31m${1}【ERROR】\33[0m"
    exit 1
}

# 启动应用
service_start(){
    [ -z "$process_num" ] && process_num=2
    for (( i = 1; i <= $process_num; i++ ));do
        /usr/bin/nohup python3  "${SERVICE_HOME}/${JAR_NAME}" > /dev/null 2>&1 &
    done
    print_success "服务启动成功"
}

# 停止应用
service_stop(){

    local pid_list=`ps -ef | grep -v "grep" | grep -v "tailf" | grep -w "$SERVICE_HOME/$JAR_NAME" | awk '{print $2}'`
    if [ -z "$pid_list" ];then
        print_warning "服务未运行"
        exit 0
    fi
    for i in $pid_list;do
        kill -9 $i
        sleep 1
    done
    while true;do
        temp_pid=`ps -ef | grep -v "grep" | grep -v "tailf" | grep -w "$SERVICE_HOME/$JAR_NAME" | awk '{print $2}'`
        if [ -z "$temp_pid" ]; then
            print_success "服务已停止"
            break
        else
            sleep 3
        fi 
    done
}

# 检查服务
service_status(){
    local temp_pid=`ps -ef | grep -v "grep" | grep -w "$SERVICE_HOME/$JAR_NAME" | awk '{print $2}'`
    if [ -z "$temp_pid" ];then
        print_msg "服务已停止"
    fi
    print_msg "服务已启动"
}

# 检查服务
service_check(){
    local temp_pid=`ps -ef | grep -v "grep" | grep -w "$SERVICE_HOME/$JAR_NAME" | awk '{print $2}'`
    if [ -z "$temp_pid" ];then
            service_start
    fi
    print_msg "服务运行正常"
}

cd $SERVICE_HOME
case "$1" in
    start)
        service_start
        ;;
    stop)
        service_stop
        ;;
    restart)
        service_stop
        service_start
        ;;
    status)
        service_status
        ;;
    check)
        service_check
        ;;
    *)
        print_warning "Usage：/bin/sh $0 start | stop | status | check 注意：start时，后面可以跟上参数代表启动几个进程"
        ;;
esac
exit 0
