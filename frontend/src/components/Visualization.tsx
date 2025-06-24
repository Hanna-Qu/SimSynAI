import React, { useState, useEffect, useRef } from 'react';
import { Card, Row, Col, Select, Button, Space, Spin, message } from 'antd';
import { BarChartOutlined, LineChartOutlined, PieChartOutlined, ReloadOutlined } from '@ant-design/icons';
import * as echarts from 'echarts';

const { Option } = Select;

interface ChartData {
  id: string;
  title: string;
  type: 'line' | 'bar' | 'pie' | 'scatter';
  data: any;
}

const Visualization: React.FC = () => {
  const [charts, setCharts] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedTask, setSelectedTask] = useState<string>('1');
  
  // Chart refs
  const lineChartRef = useRef<HTMLDivElement>(null);
  const barChartRef = useRef<HTMLDivElement>(null);
  const pieChartRef = useRef<HTMLDivElement>(null);
  const scatterChartRef = useRef<HTMLDivElement>(null);

  // 模拟数据
  const mockChartData: ChartData[] = [
    {
      id: 'performance',
      title: '性能趋势分析',
      type: 'line',
      data: {
        xAxis: {
          type: 'category',
          data: ['0s', '10s', '20s', '30s', '40s', '50s', '60s']
        },
        yAxis: {
          type: 'value',
          name: 'CPU使用率(%)'
        },
        series: [{
          name: 'CPU使用率',
          data: [20, 32, 45, 38, 52, 48, 55],
          type: 'line',
          smooth: true,
          itemStyle: { color: '#1890ff' }
        }, {
          name: '内存使用率',
          data: [15, 28, 35, 42, 38, 45, 50],
          type: 'line',
          smooth: true,
          itemStyle: { color: '#52c41a' }
        }]
      }
    },
    {
      id: 'throughput',
      title: '吞吐量统计',
      type: 'bar',
      data: {
        xAxis: {
          type: 'category',
          data: ['节点1', '节点2', '节点3', '节点4', '节点5', '节点6']
        },
        yAxis: {
          type: 'value',
          name: '吞吐量(Mbps)'
        },
        series: [{
          name: '吞吐量',
          data: [120, 200, 150, 80, 170, 110],
          type: 'bar',
          itemStyle: { color: '#722ed1' }
        }]
      }
    },
    {
      id: 'distribution',
      title: '资源分布',
      type: 'pie',
      data: {
        series: [{
          name: '资源分布',
          type: 'pie',
          radius: '60%',
          data: [
            { value: 335, name: 'CPU资源' },
            { value: 310, name: '内存资源' },
            { value: 234, name: '网络资源' },
            { value: 135, name: '存储资源' },
            { value: 148, name: '其他资源' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      }
    },
    {
      id: 'correlation',
      title: '延迟与吞吐量关系',
      type: 'scatter',
      data: {
        xAxis: {
          type: 'value',
          name: '延迟(ms)'
        },
        yAxis: {
          type: 'value',
          name: '吞吐量(Mbps)'
        },
        series: [{
          name: '数据点',
          type: 'scatter',
          data: [
            [10, 120], [15, 110], [20, 100], [25, 90], [30, 85],
            [35, 80], [40, 75], [45, 70], [50, 65], [55, 60]
          ],
          itemStyle: { color: '#fa8c16' }
        }]
      }
    }
  ];

  useEffect(() => {
    loadChartData();
  }, [selectedTask]);

  useEffect(() => {
    // 初始化图表
    if (charts.length > 0) {
      renderCharts();
    }
    
    // 窗口大小改变时重新渲染
    const handleResize = () => {
      renderCharts();
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [charts]);

  const loadChartData = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000));
      setCharts(mockChartData);
    } catch (error) {
      message.error('加载图表数据失败');
    } finally {
      setLoading(false);
    }
  };

  const renderCharts = () => {
    charts.forEach(chart => {
      let chartRef: React.RefObject<HTMLDivElement>;
      
      switch (chart.id) {
        case 'performance':
          chartRef = lineChartRef;
          break;
        case 'throughput':
          chartRef = barChartRef;
          break;
        case 'distribution':
          chartRef = pieChartRef;
          break;
        case 'correlation':
          chartRef = scatterChartRef;
          break;
        default:
          return;
      }

      if (chartRef.current) {
        const chartInstance = echarts.init(chartRef.current);
        chartInstance.setOption({
          title: {
            text: chart.title,
            left: 'center'
          },
          tooltip: {
            trigger: chart.type === 'pie' ? 'item' : 'axis'
          },
          legend: {
            top: 'bottom'
          },
          grid: chart.type !== 'pie' ? {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
          } : undefined,
          ...chart.data
        });

        // 响应式处理
        chartInstance.resize();
      }
    });
  };

  const taskOptions = [
    { value: '1', label: '基础网络仿真' },
    { value: '2', label: '大规模仿真实验' },
    { value: '3', label: '故障恢复仿真' }
  ];

  return (
    <div>
      <Card 
        title="数据可视化"
        extra={
          <Space>
            <span>选择任务：</span>
            <Select
              value={selectedTask}
              onChange={setSelectedTask}
              style={{ width: 200 }}
            >
              {taskOptions.map(option => (
                <Option key={option.value} value={option.value}>
                  {option.label}
                </Option>
              ))}
            </Select>
            <Button 
              icon={<ReloadOutlined />}
              onClick={loadChartData}
              loading={loading}
            >
              刷新
            </Button>
          </Space>
        }
      >
        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
            <p style={{ marginTop: 16 }}>正在加载图表数据...</p>
          </div>
        ) : (
          <Row gutter={[16, 16]}>
            {/* 性能趋势图 */}
            <Col xs={24} lg={12}>
              <Card 
                size="small"
                title={
                  <Space>
                    <LineChartOutlined />
                    <span>性能趋势分析</span>
                  </Space>
                }
              >
                <div 
                  ref={lineChartRef}
                  style={{ width: '100%', height: '300px' }}
                />
              </Card>
            </Col>

            {/* 吞吐量柱状图 */}
            <Col xs={24} lg={12}>
              <Card 
                size="small"
                title={
                  <Space>
                    <BarChartOutlined />
                    <span>吞吐量统计</span>
                  </Space>
                }
              >
                <div 
                  ref={barChartRef}
                  style={{ width: '100%', height: '300px' }}
                />
              </Card>
            </Col>

            {/* 资源分布饼图 */}
            <Col xs={24} lg={12}>
              <Card 
                size="small"
                title={
                  <Space>
                    <PieChartOutlined />
                    <span>资源分布</span>
                  </Space>
                }
              >
                <div 
                  ref={pieChartRef}
                  style={{ width: '100%', height: '300px' }}
                />
              </Card>
            </Col>

            {/* 散点图 */}
            <Col xs={24} lg={12}>
              <Card 
                size="small"
                title={
                  <Space>
                    <BarChartOutlined />
                    <span>延迟与吞吐量关系</span>
                  </Space>
                }
              >
                <div 
                  ref={scatterChartRef}
                  style={{ width: '100%', height: '300px' }}
                />
              </Card>
            </Col>
          </Row>
        )}
      </Card>
    </div>
  );
};

export default Visualization; 