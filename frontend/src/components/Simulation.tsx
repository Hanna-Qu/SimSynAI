import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Modal, Form, Input, Select, Tag, Space, message, Progress, Tooltip } from 'antd';
import { PlayCircleOutlined, PlusOutlined, DeleteOutlined, EyeOutlined, ReloadOutlined, ExperimentOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

const { Option } = Select;
const { TextArea } = Input;

interface SimulationTask {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  createdAt: string;
  updatedAt: string;
  parameters: Record<string, any>;
  results?: any;
}

const Simulation: React.FC = () => {
  const [tasks, setTasks] = useState<SimulationTask[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  // 模拟数据
  useEffect(() => {
    setTasks([
      {
        id: '1',
        name: '基础网络仿真',
        description: '测试基础网络拓扑的性能',
        status: 'completed',
        progress: 100,
        createdAt: '2024-01-15 10:30:00',
        updatedAt: '2024-01-15 11:45:00',
        parameters: { nodes: 10, connections: 20 }
      },
      {
        id: '2',
        name: '大规模仿真实验',
        description: '1000节点网络性能测试',
        status: 'running',
        progress: 65,
        createdAt: '2024-01-15 14:20:00',
        updatedAt: '2024-01-15 15:30:00',
        parameters: { nodes: 1000, connections: 5000 }
      },
      {
        id: '3',
        name: '故障恢复仿真',
        description: '网络故障恢复能力测试',
        status: 'failed',
        progress: 0,
        createdAt: '2024-01-15 16:10:00',
        updatedAt: '2024-01-15 16:15:00',
        parameters: { failureRate: 0.1 }
      }
    ]);
  }, []);

  const statusConfig = {
    pending: { color: 'default', text: '等待中' },
    running: { color: 'processing', text: '运行中' },
    completed: { color: 'success', text: '已完成' },
    failed: { color: 'error', text: '失败' }
  };

  const columns: ColumnsType<SimulationTask> = [
    {
      title: '任务名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <ExperimentOutlined />
          <span>{text}</span>
        </Space>
      )
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={statusConfig[status].color}>
          {statusConfig[status].text}
        </Tag>
      )
    },
    {
      title: '进度',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress, record) => (
        <Progress 
          percent={progress} 
          size="small"
          status={record.status === 'failed' ? 'exception' : 
                 record.status === 'completed' ? 'success' : 'active'}
          showInfo={record.status === 'running'}
        />
      )
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 150
    },
    {
      title: '操作',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Tooltip title="查看详情">
            <Button 
              type="text" 
              icon={<EyeOutlined />}
              onClick={() => viewTask(record)}
            />
          </Tooltip>
          {record.status === 'pending' && (
            <Tooltip title="执行任务">
              <Button 
                type="text" 
                icon={<PlayCircleOutlined />}
                onClick={() => executeTask(record.id)}
              />
            </Tooltip>
          )}
          {record.status === 'failed' && (
            <Tooltip title="重新执行">
              <Button 
                type="text" 
                icon={<ReloadOutlined />}
                onClick={() => executeTask(record.id)}
              />
            </Tooltip>
          )}
          <Tooltip title="删除任务">
            <Button 
              type="text" 
              danger
              icon={<DeleteOutlined />}
              onClick={() => deleteTask(record.id)}
            />
          </Tooltip>
        </Space>
      )
    }
  ];

  const createTask = async (values: any) => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newTask: SimulationTask = {
        id: Date.now().toString(),
        name: values.name,
        description: values.description,
        status: 'pending',
        progress: 0,
        createdAt: new Date().toLocaleString(),
        updatedAt: new Date().toLocaleString(),
        parameters: values.parameters || {}
      };
      
      setTasks(prev => [newTask, ...prev]);
      setModalVisible(false);
      form.resetFields();
      message.success('仿真任务创建成功');
    } catch (error) {
      message.error('创建任务失败');
    } finally {
      setLoading(false);
    }
  };

  const executeTask = async (taskId: string) => {
    setLoading(true);
    try {
      // 模拟执行任务
      setTasks(prev => prev.map(task => 
        task.id === taskId 
          ? { ...task, status: 'running' as const, progress: 0 }
          : task
      ));

      // 模拟进度更新
      const progressInterval = setInterval(() => {
        setTasks(prev => prev.map(task => {
          if (task.id === taskId && task.status === 'running') {
            const newProgress = Math.min(task.progress + Math.random() * 20, 100);
            const newStatus: 'completed' | 'running' = newProgress >= 100 ? 'completed' : 'running';
            return { 
              ...task, 
              progress: newProgress,
              status: newStatus,
              updatedAt: new Date().toLocaleString()
            };
          }
          return task;
        }));
      }, 1000);

      // 5秒后停止进度更新
      setTimeout(() => {
        clearInterval(progressInterval);
      }, 5000);

      message.success('任务执行已启动');
    } catch (error) {
      message.error('执行任务失败');
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = (taskId: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个仿真任务吗？',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk() {
        setTasks(prev => prev.filter(task => task.id !== taskId));
        message.success('任务已删除');
      }
    });
  };

  const viewTask = (task: SimulationTask) => {
    Modal.info({
      title: '任务详情',
      width: 600,
      content: (
        <div>
          <p><strong>任务名称：</strong>{task.name}</p>
          <p><strong>描述：</strong>{task.description}</p>
          <p><strong>状态：</strong>
            <Tag color={statusConfig[task.status].color}>
              {statusConfig[task.status].text}
            </Tag>
          </p>
          <p><strong>进度：</strong>{task.progress}%</p>
          <p><strong>创建时间：</strong>{task.createdAt}</p>
          <p><strong>更新时间：</strong>{task.updatedAt}</p>
          <p><strong>参数：</strong></p>
          <pre style={{ backgroundColor: '#f5f5f5', padding: 8, borderRadius: 4 }}>
            {JSON.stringify(task.parameters, null, 2)}
          </pre>
        </div>
      )
    });
  };

  return (
    <div>
      <Card 
        title="仿真任务管理"
        extra={
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={() => setModalVisible(true)}
          >
            创建任务
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={tasks}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 条记录`
          }}
        />
      </Card>

      {/* 创建任务模态框 */}
      <Modal
        title="创建仿真任务"
        open={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        confirmLoading={loading}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={createTask}
        >
          <Form.Item
            name="name"
            label="任务名称"
            rules={[{ required: true, message: '请输入任务名称' }]}
          >
            <Input placeholder="输入任务名称" />
          </Form.Item>

          <Form.Item
            name="description"
            label="任务描述"
            rules={[{ required: true, message: '请输入任务描述' }]}
          >
            <TextArea rows={3} placeholder="输入任务描述" />
          </Form.Item>

          <Form.Item
            name="type"
            label="仿真类型"
            rules={[{ required: true, message: '请选择仿真类型' }]}
          >
            <Select placeholder="选择仿真类型">
              <Option value="network">网络仿真</Option>
              <Option value="performance">性能测试</Option>
              <Option value="fault">故障仿真</Option>
              <Option value="custom">自定义</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="parameters"
            label="仿真参数"
          >
            <TextArea 
              rows={4} 
              placeholder="输入JSON格式的参数，例如：&#10;{&#10;  &quot;nodes&quot;: 100,&#10;  &quot;connections&quot;: 200&#10;}"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Simulation; 