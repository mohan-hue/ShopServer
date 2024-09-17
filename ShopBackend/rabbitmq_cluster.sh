#!/bin/bash
RABBITMQ_NODE_NAME=rabbit@$HOSTNAME

# 等待 RabbitMQ 启动
# 等待 RabbitMQ 完全启动
echo "Waiting for RabbitMQ to start..."
until rabbitmqctl status; do
  echo "RabbitMQ is not ready, waiting..."
  sleep 5
done
# 固定的用户和密码
NEW_USER="root"
NEW_PASSWORD="123456"
# 添加固定的用户
rabbitmqctl add_user $NEW_USER $NEW_PASSWORD

# 设置用户的管理员权限
rabbitmqctl set_user_tags $NEW_USER administrator
rabbitmqctl set_permissions -p / $NEW_USER ".*" ".*" ".*"

# 假设 rabbitmq1 是集群中的第一个节点，其他节点通过此节点加入集群
if [ "$HOSTNAME" != "rabbit@wh-virtual-machine" ]; then
  rabbitmqctl stop_app
  rabbitmqctl join_cluster rabbit@wh-virtual-machine
  rabbitmqctl start_app
fi

