import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Select, Space, Typography, Divider, Row, Col } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, GlobalOutlined } from '@ant-design/icons';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const { Text, Title } = Typography;
const { Option } = Select;

interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export interface RegisterProps {
  onRegister: (data: RegisterFormData) => Promise<void>;
}

const Register: React.FC<RegisterProps> = ({ onRegister }) => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();

  const onFinish = async (values: RegisterFormData) => {
    if (values.password !== values.confirmPassword) {
      message.error(t('auth.passwordMismatch') || '两次输入的密码不一致');
      return;
    }

    setLoading(true);
    try {
      // 调用真实的注册API
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: values.username,
          email: values.email,
          password: values.password
        })
      });

      if (response.ok) {
        const data = await response.json();
        message.success(t('auth.registerSuccess') || '注册成功，请登录');
        navigate('/login');
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || t('auth.registerError') || '注册失败，请稍后再试');
      }
    } catch (error) {
      message.error(t('auth.registerError') || '注册失败，请检查网络连接');
    } finally {
      setLoading(false);
    }
  };

  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('language', lang);
  };

  return (
    <div className="auth-container">
      {/* 顶部导航栏 */}
      <div className="auth-header">
        <Row justify="space-between" align="middle" style={{ width: '100%', maxWidth: '1200px' }}>
          <Col>
            <div className="auth-logo">
              <Title level={2} style={{ color: '#fff', margin: 0 }}>
                SimSynAI
              </Title>
              <Text style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px' }}>
                {t('common.subtitle') || 'AI智能仿真平台'}
              </Text>
            </div>
          </Col>
          <Col>
            <Select
              value={i18n.language}
              onChange={changeLanguage}
              style={{ width: 120 }}
              suffixIcon={<GlobalOutlined style={{ color: '#fff' }} />}
              className="language-selector"
            >
              <Option value="zh">中文</Option>
              <Option value="en">English</Option>
            </Select>
          </Col>
        </Row>
      </div>

      {/* 主要内容区域 */}
      <div className="auth-content">
        <Card 
          title={t('auth.register') || '用户注册'} 
          className="auth-card"
        >
          <Form
            name="register"
            onFinish={onFinish}
            autoComplete="off"
            size="large"
          >
            <Form.Item
              name="username"
              rules={[{ required: true, message: t('auth.usernameRequired') || '请输入用户名!' }]}
            >
              <Input 
                prefix={<UserOutlined />} 
                placeholder={t('auth.username') || '用户名'} 
              />
            </Form.Item>

            <Form.Item
              name="email"
              rules={[
                { required: true, message: t('auth.emailRequired') || '请输入邮箱!' },
                { type: 'email', message: '请输入有效的邮箱地址!' }
              ]}
            >
              <Input 
                prefix={<MailOutlined />} 
                placeholder={t('auth.email') || '邮箱'} 
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[
                { required: true, message: t('auth.passwordRequired') || '请输入密码!' },
                { min: 6, message: '密码长度至少为6个字符!' }
              ]}
            >
              <Input.Password 
                prefix={<LockOutlined />} 
                placeholder={t('auth.password') || '密码'} 
              />
            </Form.Item>

            <Form.Item
              name="confirmPassword"
              rules={[{ required: true, message: t('auth.confirmPasswordRequired') || '请确认密码!' }]}
            >
              <Input.Password 
                prefix={<LockOutlined />} 
                placeholder={t('auth.confirmPassword') || '确认密码'} 
              />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading} block size="large">
                {t('auth.register') || '注册'}
              </Button>
            </Form.Item>

            <Divider plain>{t('auth.hasAccount') || '已有账号？'}</Divider>

            <Form.Item>
              <Button 
                block 
                size="large"
                onClick={() => navigate('/login')}
                className="auth-secondary-btn"
              >
                {t('auth.login') || '立即登录'}
              </Button>
            </Form.Item>
          </Form>
        </Card>
      </div>

      {/* 底部信息 */}
      <div className="auth-footer">
        <Text style={{ color: 'rgba(255,255,255,0.8)' }}>
          {t('footer.copyright') || 'SimSynAI © 2024 基于大语言模型的智能化仿真平台'}
        </Text>
      </div>
    </div>
  );
};

export default Register;

