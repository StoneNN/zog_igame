import React from 'react';
import { Flex, WhiteSpace, InputItem, Toast, Button, NavBar, Icon } from 'antd-mobile';
import './Login.css'
import 'antd-mobile/dist/antd-mobile.css'; // 这一句是从哪里引入的？
import { createForm } from 'rc-form';
import Models from '../Models/Models';
import session from './session';

export default class LoginPage extends React.Component{
   render () {
       return(
        <div className="flex-container">
            <NavBar
                mode="light"
                icon={<Icon type="left" />}
                onLeftClick={this.props.goHome}
                >
            </NavBar>
            <Flex direction='column'>
                <img alt='log' src={require("./963065731.jpg")} style={{width:360,marginTop:-30}}/>
                <WhiteSpace size="lg" />

                <LoginForm toggleLoginState={this.props.toggleLoginState} />
                <WhiteSpace size="sm" />

                <p className='text'>登录即代表您已同意<a>《智赛桥牌隐私政策》</a></p>
                <WhiteSpace size="xl" />
                <WhiteSpace size="xl" />
                <WhiteSpace size="xl" />

                <Flex align="baseline">
                    <button className='btn1' onClick={this.props.toRegisterpage} >点击注册</button>
                    <p className='login-p'>|</p>
                    <button className='btn1' onClick={this.props.toFindPwdpage} >忘记密码</button>
                </Flex>
                <WhiteSpace size="lg" />
            </Flex>
        </div>
       );
   } 
}

class BasicInput extends React.Component {   //输入组件，经过下面的createForm()变成可提交的组件
    componentDidMount() {
    //   this.autoFocusInst.focus();
    }
    onSubmit = () => {   //表单提交方法
        this.props.form.validateFields({ force: true }, (error) => {  //输入验证，符合规则才向后后端交数据
            if (!error) {
                var formData = this.props.form.getFieldsValue();  //表单数据
                const json = {  //向后端提交的数据
                    'db':'TT',
                    'login': formData.phone,  
                    'password': formData.password,
                }
                const cb = (data)=>{
                    if (data.sid){
                        session.set_sid(data.sid)
                        Toast.success("登录成功！",1);
                        // this.callback();
                        this.props.toggleLoginState();   //修改最外层的组件的登录状态（此方法经App.js-->User/Index.js-->到本组件）
                    }else{
                        Toast.fail('登录失败，请稍后重试！',1);
                    }
                }
                const m = Models.create();
                // m.query('login',json123,cb);
                m.query('login',json,cb);
                // this.props.toggleLoginState()   //修改最外层的组件的登录状态（此方法经App.js-->User/Index.js-->到本组件）

            } else {
                Toast.fail('您的输入不完整！');
            }
        });
      }
    
    validateAccount = (rule, value, callback) => {  //输入验证规则
        if (value && value.replace(/\s/g, '').length < 11) {
          callback(new Error('Please enter 11 digits'));
        } else {
          callback();
        }
      }
    render() {
        const { getFieldProps, getFieldError } = this.props.form;
        return (
            <form>
                <InputItem
                    {...getFieldProps('phone',{
                        rules: [
                            { required: true, message: '手机号尚未填写！' },
                            { validator: this.validateAccount },
                        ],
                    })}
                    clear
                    error={!!getFieldError('phone')}
                    onErrorClick={() => {
                        Toast.info(getFieldError('phone').join('、'));
                    }}
                    type="phone"
                    placeholder="enter your phone"
                >手机号</InputItem>
                <InputItem
                    {...getFieldProps('password',{
                        rules: [
                            { required: true, message: '密码不能为空！' },
                        ],
                    })}
                    type="password"
                    placeholder="******"
                >  密码</InputItem>
                <WhiteSpace size="xl" />
                <WhiteSpace size="xl" />
                <Button type=""  onClick={this.onSubmit} className='login-btn'>登录</Button>
            </form>
        );
    }
  }
  const LoginForm = createForm()(BasicInput);  //表单组件



  