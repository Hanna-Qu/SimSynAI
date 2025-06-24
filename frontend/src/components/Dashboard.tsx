import React from 'react';
import { Card, Row, Col, Statistic, Typography } from 'antd';
import { UserOutlined, ExperimentOutlined, MessageOutlined, AreaChartOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';

const { Title } = Typography;

const Dashboard: React.FC = () => {
  // const { t } = useTranslation();
  
  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>仪表板</Title>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="用户数量"
              value={1128}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="仿真实验"
              value={93}
              prefix={<ExperimentOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="对话次数"
              value={456}
              prefix={<MessageOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="数据分析"
              value={78}
              prefix={<AreaChartOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>
      
      <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
        <Col xs={24} lg={12}>
          <Card title="最近活动" style={{ height: '300px' }}>
            <p>系统运行正常</p>
            <p>最近登录时间: {new Date().toLocaleString()}</p>
          </Card>
        </Col>
        
        <Col xs={24} lg={12}>
          <Card title="系统状态" style={{ height: '300px' }}>
            <p>CPU使用率: 45%</p>
            <p>内存使用率: 60%</p>
            <p>磁盘使用率: 30%</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 