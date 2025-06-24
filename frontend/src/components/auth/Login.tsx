import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Checkbox, Select, Space, Typography, Divider, Row, Col } from 'antd';
import { UserOutlined, LockOutlined, GlobalOutlined } from '@ant-design/icons';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import '../../styles/auth.css';

const { Text, Title } = Typography;
const { Option } = Select;

interface LoginProps {
  onLogin: (loginData: { username: string; password: string }) => Promise<void>;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { t, i18n } = useTranslation();
  
  const from = location.state?.from?.pathname || '/dashboard';

  const onFinish = async (values: { username: string; password: string; remember: boolean }) => {
    setLoading(true);
    try {
      // 调用真实的登录API
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: values.username,
          password: values.password
        })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('username', values.username);
        if (values.remember) {
          localStorage.setItem('remember', 'true');
        }
        
        await onLogin(values);
        message.success(t('login.loginSuccess') || '登录成功');
        navigate(from, { replace: true });
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || t('login.loginError') || '登录失败');
      }
    } catch (error) {
      message.error(t('login.loginError') || '登录失败，请检查网络连接');
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
          title={t('login.title') || '用户登录'} 
          className="auth-card"
        >
          <Form
            name="login"
            onFinish={onFinish}
            autoComplete="off"
            size="large"
          >
            <Form.Item
              name="username"
              rules={[{ required: true, message: t('login.usernameRequired') || '请输入用户名或邮箱!' }]}
            >
              <Input 
                prefix={<UserOutlined />} 
                placeholder={t('login.username') || '用户名或邮箱'} 
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[{ required: true, message: t('login.passwordRequired') || '请输入密码!' }]}
            >
              <Input.Password 
                prefix={<LockOutlined />} 
                placeholder={t('login.password') || '密码'} 
              />
            </Form.Item>

            <Form.Item>
              <Row justify="space-between" align="middle">
                <Col>
                  <Form.Item name="remember" valuePropName="checked" noStyle>
                    <Checkbox>{t('login.rememberMe') || '记住我'}</Checkbox>
                  </Form.Item>
                </Col>
                <Col>
                  <Link to="/forgot-password" className="auth-link">
                    {t('login.forgotPassword') || '忘记密码'}
                  </Link>
                </Col>
              </Row>
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading} block size="large">
                {t('login.loginButton') || '登录'}
              </Button>
            </Form.Item>

            <Divider plain>{t('login.noAccount') || '还没有账号？'}</Divider>

            <Form.Item>
              <Button 
                block 
                size="large"
                onClick={() => navigate('/register')}
                className="auth-secondary-btn"
              >
                {t('login.registerNow') || '立即注册'}
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

export default Login; 