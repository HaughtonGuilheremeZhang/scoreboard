import time
import pymssql
import wx
import wx.xrc
#连接数据库的配置
serverName = 'DESKTOP-RO1OVQP\SQLEXPRESS'    #目的主机ip地址或主机名
userName = 'sa'        #SQL Server身份账号
passWord = '123'        #SQL Server身份密码
dbName = '体育赛事计分系统'        #对应数据库名称

def OUT_PUT(rows):#输出模块
    s1 = ''#传入一个来自数据库的元组，返回一个特定格式的字符串，可以选择在文本框或控制台中输出
    for k in rows:
        for k1 in k:
            s1 += (str(k1).strip(' ')) +"           \t"
        s1 += '\n'
    if s1 == '':
        s1='空信息'
    #print(s1)
    return s1
#程序模块
#使用者类
class user(object):
   user_name=" "

   user_password=" "

   def user_identity(self,db,user_name,user_password):#识别用户权限，是管理员还是普通用户
       sql='select* from 用户3121005409张皓 where 用户名='+"'"+user_name+"'"
       rows=database.execute_sql(db, sql)
       #可能查找不到，判空
       if len(rows)==0:
           return 'error'

       n=rows[0][1].rstrip()#去除字符串后的空格
       if n==user_password:
           uid=rows[0][2];
       else:
           uid='error'#出错控制，通常是查不到用户，或密码错误

       return uid

   def select(self,db,table_name,column_name):#用户的查看方法，传入数据库，表名，排序列名
        if column_name=="null":
                sql = 'select* from '+table_name
        else:
                sql = 'select* from ' + table_name + ' order by '+column_name + ' desc;'

        rows = database.execute_sql(db,sql)
        database.get_column_name(db,table_name)
        s1=OUT_PUT(rows)
        return s1

#数据库类
class database(object):

    #初始化
    def __init__(self, url, username, password, databaseName, port, charset):
        self.url = url
        self.username = username
        self.password = password
        self.databaseName = databaseName
        self.port = port
        self.charset = charset
        self.connect = self.sql_server_conn()
        self.cursor = self.connect.cursor()
    #连接函数
    def sql_server_conn(self):
        connect = pymssql.connect(self.url, self.username, self.password, self.databaseName, port=self.port,
                                  charset=self.charset)  # 服务器名,账户,密码,数据库名
        if connect:
            print(u"连接成功！")
        else:
            print("connectted failed")
        return connect

        # 查看表的所有字段，
        # @table_name :表名
    def get_column_name(self, table_name):
        self.cursor.execute("select top 1 * from " + table_name)  # 执行sql语句
        data_dict = []
        for field in self.cursor.description:
            data_dict.append(field[0])
        print(data_dict)
        return data_dict

        # 得到数据库所有的表名
    def get_table_name(self):
        sql = "SELECT NAME FROM SYSOBJECTS WHERE XTYPE='U' ORDER BY NAME"
        self.cursor.execute(sql)  # 返回执行成功的结果条数
        rows = self.cursor.fetchall()

    #用来执行sql语句的函数,查询则返回结果,其他功能则返回空值
    def execute_sql(self, sql):
        try:
            sql = sql.lower()
            if 'insert' in sql or 'delete' in sql or 'update' in sql:#增删改执行后显示表的结果
                self.cursor.execute(sql)
                self.connect.commit()
                if '赛事3121005409张皓'in sql:
                    sql2='select* from 赛事3121005409张皓;'
                    self.cursor.execute(sql2)
                    rows = self.cursor.fetchall()
                if '球员3121005409张皓'in sql:
                    sql2='select* from 球员3121005409张皓;'
                    self.cursor.execute(sql2)
                    rows = self.cursor.fetchall()
                if '球队3121005409张皓'in sql:
                    sql2='select* from 球队3121005409张皓;'
                    self.cursor.execute(sql2)
                    rows = self.cursor.fetchall()
                if '积分榜3121005409张皓'in sql:
                    sql2='select* from 积分榜3121005409张皓 order by 积分 desc;'
                    self.cursor.execute(sql2)
                    rows = self.cursor.fetchall()
                if '射手榜'in sql:
                    sql2='select* from 射手榜 order by 进球数 desc;'
                    self.cursor.execute(sql2)
                    rows = self.cursor.fetchall()
                if '助攻榜'in sql:
                    sql2='select* from 助攻榜 order by 助攻数 desc;'
                    self.cursor.execute(sql2)
                    rows = self.cursor.fetchall()
            elif 'select' in sql:#选择语句
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()

            return rows
        except :
            #print("输入sql语句错误！")
            frame.result_label.SetLabel("输入sql语句错误！请重新输入！")

    def close(self):
         self.cursor.close()  # 关闭游标
         self.connect.close()
#操作界面
class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        #为窗口添加控件
        super(MyFrame, self).__init__(*args, **kw)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(wx.Font(9, 70, 90, 90, False, "宋体"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)
        #查看按钮控件
        self.select_button = wx.Button(self, wx.ID_ANY, u"查看", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.select_button, 0, wx.ALL, 5)
        #确定按钮
        self.confirm_button = wx.Button(self, wx.ID_ANY, u"sql语句确认", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.confirm_button, 0, wx.ALL, 5)

        fgSizer1.Add(bSizer5, 1, wx.EXPAND, 5)
        #列表控件用于选择查看信息
        m_listBox3Choices = ['已收录赛事', '已收录球员', '已收录球队', '积分榜', '射手榜', '助攻榜']
        self.m_listBox3= wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(230, 300), m_listBox3Choices, 0)
        fgSizer1.Add(self.m_listBox3, 0, wx.ALL, 5)

        bSizer7.Add(fgSizer1, 1, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"语句输入框", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        self.m_staticText4.SetFont(wx.Font(9, 70, 90, 90, False, "宋体"))

        bSizer6.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.input_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(354, 30), 0)
        bSizer6.Add(self.input_text, 0, wx.ALL, 5)

        self.result_label = wx.StaticText(self, wx.ID_ANY, u"结果：", wx.DefaultPosition, wx.Size(370, 370), 0)
        self.result_label.Wrap(-1)
        bSizer6.Add(self.result_label, 0, wx.ALL, 5)

        bSizer7.Add(bSizer6, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer7)
        self.Layout()

        self.Centre(wx.BOTH)

        #绑定控件与事件

        #self.calculate_button = wx.Button(self.panel, label="查询")
        self.m_listBox3.Bind(wx.EVT_LISTBOX, self.func)
        self.select_button.Bind(wx.EVT_BUTTON,self.func)
        self.confirm_button.Bind(wx.EVT_BUTTON,self.govn)
    def govn(self,event):#管理员使用sql语句对数据库进行编辑
        uid=user.user_identity(us1, con, us1.user_name, us1.user_password)
        uid = uid.rstrip()

        if uid=='管理员':
            value = self.input_text.GetValue()
            rows=database.execute_sql(con,value)
            s1=OUT_PUT(rows)
            self.result_label.SetLabel(s1)
        elif uid=='普通用户':
            self.result_label.SetLabel("你是普通用户，无法使用此功能！！")

        else:
            self.result_label.SetLabel("身份认证出错！")

    def func(self, event):
        key=event.GetString()
        #['已收录赛事', '已收录球员', '已收录球队', '积分榜', '射手榜', '助攻榜']
        if key == '已收录赛事':
            s1 = user.select(us1, con, '赛事3121005409张皓','null')
            self.result_label.SetLabel(s1)

        elif key =='已收录球员':
            s1 = user.select(us1, con, '球员3121005409张皓','null')
            self.result_label.SetLabel(s1)

        elif key == '已收录球队':
            s1 = user.select(us1, con, '球队3121005409张皓','null')
            self.result_label.SetLabel(s1)

        elif key == '积分榜':
            s1 = user.select(us1, con, '积分榜3121005409张皓','积分')
            self.result_label.SetLabel(s1)

        elif key == '射手榜':
            s1 = user.select(us1, con, '射手榜','进球数')
            self.result_label.SetLabel(s1)

        elif key == '助攻榜':
            s1 = user.select(us1, con, '助攻榜','助攻数')
            self.result_label.SetLabel(s1)
#登陆界面
class Governlogin(wx.Dialog):
    def __init__(self, *args, **kw):
        #wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          # size=wx.Size(420, 313), style=wx.DEFAULT_DIALOG_STYLE)
        super(Governlogin, self).__init__(*args, **kw)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"用户名", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        bSizer3.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.user_name_input = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, 30), 0)
        bSizer3.Add(self.user_name_input, 0, wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"密码", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        bSizer3.Add(self.m_staticText6, 0, wx.ALL, 5)

        self.user_password_input = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                   wx.Size(400, 30), 0)
        bSizer3.Add(self.user_password_input, 0, wx.ALL, 5)

        self.conf_button = wx.Button(self, wx.ID_ANY, u"确认", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer3.Add(self.conf_button, 0, wx.ALL, 5)

        self.rl = wx.StaticText(self, wx.ID_ANY,u"登录反馈栏：                    ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.rl.Wrap(-1)

        bSizer3.Add(self.rl, 0, wx.ALL, 5)

        #self.disp = wx.StaticText(self, wx.ID_ANY,u"   ", wx.DefaultPosition, wx.DefaultSize, 0)
        #self.disp.Wrap(-1)
        #bSizer3.Add(self.disp, 0, wx.ALL, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)
        #绑定事件
        self.conf_button.Bind(wx.EVT_BUTTON,self.action)

    def action(self,event):
        user_name=self.user_name_input.GetValue()
        user_password=self.user_password_input.GetValue()
        uid=user.user_identity(us1,con,user_name,user_password)#传回rows
        us1.user_name = user_name  # 将用户姓名写回实例属性中
        us1.user_password = user_password  # 将用户密码写回实例属性中，即使窗口进程结束也可在下一进程中使用
        uid = uid.rstrip()
        if uid=='管理员':
            self.rl.SetLabel("以管理员身份登录！")
            time.sleep(2)  # 按下确认按钮后，发现是正确的，等待一段时间后（3s），关闭此弹窗
            self.Destroy()  # 结束登录窗口进程
        elif uid=='普通用户':
            self.rl.SetLabel("以普通用户身份登录！")
            time.sleep(2)  # 按下确认按钮后，发现是正确的，等待一段时间后（3s），关闭此弹窗
            self.Destroy()  # 结束登录窗口进程
        else:self.rl.SetLabel("用户名错误或密码错误！！")



if __name__ == '__main__':
    us1 = user()#实例化用户

    con = database(serverName, userName, passWord, dbName, '49680', 'utf8')#实例化数据库
    app = wx.App(False)

    dialog=Governlogin(None,title="登录界面",size=(420, 313))#运行弹窗
    dialog.ShowModal()

    frame = MyFrame(None, title="体育赛事计分系统", size=(378, 688))#实例化界面
    frame.Show()
    app.MainLoop()






