#!/bin/bash
#====================================================================
# sched_persist.sh
#
# Fxt Spiders Start Script
#
#====================================================================

# 加载必要的环境变量
source /etc/profile
source /root/.bashrc

# 自定义常量
SERVICE_NAME="FxtDataAcquisition"
SERVICE_HOME="/usr/local/${SERVICE_NAME}/${SERVICE_NAME}/scheduler"
JOB_NAME="sched_persist_cases.py"
LOG_PATH="/var/log/${JOB_NAME}.log"

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

    local temp_pid=`ps -ef | grep -v "grep" | grep -w "$SERVICE_HOME/$JOB_NAME" | awk '{print $2}'`
    if [ "$temp_pid" != "" ];then
        print_error "请先停止服务之后再启动服务"
    fi
    /usr/bin/nohup python3  "${SERVICE_HOME}/${JOB_NAME}" > /dev/null 2>&1 &
    if [ "$?" -ne 0 ];then
        print_error "服务启动失败"
    else
        print_success "服务已启动"
    fi
    
}

# 停止应用
service_stop(){

    local temp_pid=`ps -ef | grep -v "grep" | grep -w "$SERVICE_HOME/$JOB_NAME" | awk '{print $2}'`
        if [ -z "$temp_pid" ];then
            print_warning "服务未运行"
            exit 0
        fi

        kill $temp_pid
        sleep 10

        while true
            do
                temp_pid=`ps -ef | grep -v "grep" | grep -w "$SERVICE_HOME/$JOB_NAME" | awk '{print $2}'`
                if [ -z "$temp_pid" ]; then
                    print_success "服务已停止"
                    break
                else
                    sleep 5
                fi 
            done
    
}

# 检查服务
service_status(){
    local temp_pid=`ps -ef | grep -v "grep" | grep -w "$SERVICE_HOME/$JOB_NAME" | awk '{print $2}'`
    if [ -z "$temp_pid" ];then
        print_msg "服务已停止"
    else
        print_msg "服务已启动"
    fi
}

# 检查服务
service_check(){
    local temp_pid=`ps -ef | grep -v "grep" | grep -w "$SERVICE_HOME/$JOB_NAME" | awk '{print $2}'`
    if [ -z "$temp_pid" ];then
            service_start
    else
        print_msg "服务运行正常"
    fi
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
        print_warning "Usage：/bin/sh $0 start | stop | restart"
        ;;
esac
exit 0
