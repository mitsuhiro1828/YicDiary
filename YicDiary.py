from cgitb import text
import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors

WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
class YicLogin:
  def __init__(self, root, connection, Error=None):

    root.title('予定管理アプリ ログイン画面')
    root.geometry('520x280')
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None
    frame1 = tk.Frame(root)
    frame1.grid()
    
    label1 = tk.Label(frame1, text='苗字')
    label1.grid(row=0, column=0)
    
    label2 = tk.Label(frame1, text='名前')
    label2.grid(row=1, column=0)
      
    label3 = tk.Label(frame1, text='パスワード')
    label3.grid(row=2, column=0)

    FamilyName = tk.StringVar()
    FamilyName_entry = tk.Entry(
      frame1,
      textvariable=FamilyName,
      width=20)
    FamilyName_entry.grid(row=0, column=1)

    FirstName = tk.StringVar()
    FirstName_entry= tk.Entry(
      frame1,
      textvariable=FirstName,
      width=20)
    FirstName_entry.grid(row=1, column=1)

    Password = tk.StringVar()
    Password_entry = tk.Entry(
      frame1,
      textvariable=Password,
      width=20,
      show='*')
    Password_entry.grid(row=2, column=1)

    frame2 =tk.Frame(frame1)
    frame2.grid(row=3, column=1)

    button_login = tk.Button(
      frame2, text='ログイン',
      command=lambda:self.Certification(root, connection, FamilyName.get(), FirstName.get(), Password.get()))
    # ↑commandはlambdaを使わないとボタンを押さなくてもcommandが発動されてエラーが起こる
    button_login.grid(row=0, column=0)

    button_entry = tk.Button(
      frame2, text='新規登録',
      command=lambda:self.Register(root, connection,)
    )
    button_entry.grid(row=0, column=1)
    if Error is not None:
      label_Error = tk.Label(frame2, text=Error)
      label_Error.grid(row=1, column=0)

  def Register(self, root, connection):
    root.destroy()
    root = tk.Tk()
    Register(root, connection)


  def Certification(self, root, connection, FamilyName, FirstName, Password):
    try:
      with connection.cursor() as cursor:
        cursor = connection.cursor()
        sql = "select *\
              from Members\
              where FamilyName = %s and FirstName = %s and Password = %s"
        cursor.execute(sql, (FamilyName, FirstName, Password))
        results = cursor.fetchall()
        for i in results:
          userID = f"{i['MembersID']}"
        # 結果の受け取り
        # root内のウィジットを全廃棄
        root.destroy()
        root = tk.Tk()
        YicDiary(root, connection, userID)
    except Exception as e:
      print(e)
      Error = '登録情報が間違っています。もう一度やり直してください'
      root.destroy()
      root = tk.Tk()
      YicLogin(root, connection, Error)

class Register:
  def __init__(self, root, connection, Error=None):
    root.title('予定管理アプリ 新規登録画面')
    root.geometry('520x280')
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None
    frame1 = tk.Frame(root)
    frame1.grid()
    label = tk.Label(frame1, text='登録情報を入力してください。')
    label.grid(row=0, column=0)
    label1 = tk.Label(frame1, text='苗字')
    label1.grid(row=1, column=0)
    
    label2 = tk.Label(frame1, text='名前')
    label2.grid(row=2, column=0)
      
    label3 = tk.Label(frame1, text='パスワード')
    label3.grid(row=3, column=0)

    FamilyName = tk.StringVar()
    FamilyName_entry = tk.Entry(
      frame1,
      textvariable=FamilyName,
      width=20)
    FamilyName_entry.grid(row=1, column=1)

    FirstName = tk.StringVar()
    FirstName_entry= tk.Entry(
      frame1,
      textvariable=FirstName,
      width=20)
    FirstName_entry.grid(row=2, column=1)

    Password = tk.StringVar()
    Password_entry = tk.Entry(
      frame1,
      textvariable=Password,
      width=20,
      show='*')
    Password_entry.grid(row=3, column=1)
    frame2 =tk.Frame(frame1)
    frame2.grid(row=4, column=1)
    button = tk.Button(
      frame2, text='登録',
      command=lambda:self.NewRegister(root, connection, FamilyName.get(), FirstName.get(), Password.get()))
    button.grid(row=1, column=0)
    if Error is not None:
      label_Error = tk.Label(frame2, text=Error)
      label_Error.grid(row=2, column=0)

  def NewRegister(self, root, connection, FamilyName, FirstName, Password):
    if FamilyName == '' or FirstName == '' or Password == '':
      Error = '※登録情報に空白があります。もう一度やり直してください'
      root.destroy()
      root = tk.Tk()
      Register(root, connection, Error)

    
    else:
      
        with connection.cursor() as cursor:
          cursor = connection.cursor()
          sql = "select *\
                from Members\
                where FamilyName = %s and FirstName = %s and Password = %s"
          cursor.execute(sql, (FamilyName, FirstName, Password))
          results = cursor.fetchone()
          if results is None:
            sql = 'insert into members (FamilyName, FirstName, Password)\
                values (%s, %s, %s)'
            cursor.execute(sql, (FamilyName, FirstName, Password))
            connection.commit()
            root.destroy()
            root = tk.Tk()
            YicLogin(root, connection)
          else:
            Error = 'すでに登録者がいます。パスワード等を変えてやり直してください。'
            root.destroy()
            root = tk.Tk()
            Register(root, connection, Error)




class YicDiary:
  def __init__(self, root, connection,  userID):
    self.connection = connection
    self.UserID = userID
    root.title('予定管理アプリ')
    root.geometry('520x280')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame, root)
    leftFrame2 = tk.Frame(root)
    leftFrame2.grid(row=1, column=0)
    with connection.cursor() as cursor:
      cursor = connection.cursor()
      sql = "select FamilyName, FirstName\
                from Members\
                where MembersID = %s"
      cursor.execute(sql, (userID))
      results = cursor.fetchone()
    label_LoginName = tk.Label(leftFrame2, text=f'{results["FamilyName"]}{results["FirstName"]}がログイン')
    label_LoginName.grid(row=0, column=0)
    

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1)
    self.rightBuild(rightFrame)
    self.Text = tk.StringVar()
    self.Text.set('予定なし')

    self.root = root
    self.rightFrame1 = tk.Frame(self.root)
    self.rightFrame1.grid(row=1, column=1)
    
  
    self.actions_dic = []
    self.actions_list = []
    try:
      with connection.cursor() as cursor:
        cursor = connection.cursor()
        sql = "select * from Kinds"
        cursor.execute(sql)
      # 結果の受け取り
        results = cursor.fetchall()
        for i in results:
          self.actions_dic.append(i)
          self.actions_list.append(f"{i['Kind']}")
    except Exception as e:
      print('error:', e)


  #-----------------------------------------------------------------






  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame, root):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    self.disp(0, root)


  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)

    button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
    button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)

    self.schedule()


  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    # ウィジットを廃棄
    for widget in self.r2_frame.winfo_children():
      widget.destroy()
    # データベースに予定の問い合わせを行う
    pass


  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv, root):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1


    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)

      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=self.actions_list)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()


  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
    # データベースに新規予定を挿入する
    # 日付
    days = '{}-{}-{}'.format(self.year, self.mon, self.today)

    # 種別
    Kinds = self.combo.get()
    Contents = self.text.get('1.0', 'end-1c')
    try:
      # トランザクション開始
      self.connection.begin()

      with self.connection.cursor() as cursor:
        cursor = self.connection.cursor()
        '''
        sql = "select * from schedule"
        cursor.execute(sql)
        '''

        KindsID = ''
        for i in self.actions_dic:
          if i['Kind'] == Kinds:
            KindsID = i['KindsID']

        # SQLの作成、定義
        sql = "insert into schedule(MembersID, kindsID, contents) value (%s, %s, %s)"
        # SQLの実行
        cursor.execute(sql, (self.UserID, KindsID, Contents))
        '''
        # 実行結果の受け取り（複数行） 
        results = cursor.fetchall()
        for i, row in enumerate(results):
          print(i, row)
        '''
        # SQLの作成、定義
        sql1 = "select Max(ScheduleID) from schedule"
        cursor.execute(sql1)
        for i in cursor.fetchone().values():
          MaxScheduleID = i
        
        # SQLの作成、定義
        sql2 = "insert into scheduletable(Date, ScheduleID) value(%s, %s)"
        cursor.execute(sql2, (days, MaxScheduleID))
        # 実行結果の受け取り（複数行） 
        results = cursor.fetchall()
        for i, row in enumerate(results):
          print(i, row)

        self.connection.commit()
      self.sub_win.destroy()
    except Exception as e:
      print('error:', e)
      self.connection.rollback()

      


  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    self.rightFrame1.destroy()
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day
      # SQLの作成
      # \ = エスケープシーケンス
    try:
      with self.connection.cursor() as cursor:

        cursor = self.connection.cursor()
        # トランザクション開始
        sql = "select FamilyName, FirstName, Kind, Contents\
              from scheduletable\
              inner join schedule\
              on scheduletable.scheduleID = schedule.scheduleID\
              inner join Kinds\
              on schedule.KindsID = Kinds.KindsID\
              inner join members\
              on schedule.MembersID = members.MembersID\
              where Date = '%s-%s-%s'"
        cursor.execute(sql, (self.year, self.mon, self.today))
        # 実行結果の受け取り（複数行） 
        results = cursor.fetchall()
        LabelText = []
        self.rightFrame1 = tk.Frame(self.root)
        self.rightFrame1.grid(row=1, column=1)

        for j in results:
          LabelText.append(f"{j['FamilyName']}{j['FirstName']} ： (種別){j['Kind']}  (内容){j['Contents']}")
        if LabelText == []:
          Label_1 = tk.Label(self.rightFrame1, text='予定なし')
          Label_1.grid(row=0, column=0)
        else:
          for i, j  in enumerate(LabelText):
            Label_1 = tk.Label(self.rightFrame1, text=j)
            Label_1.grid(row=i, column=0)
            


          
    except Exception as e:
      print('error:', e)


def Main():
  root = tk.Tk()
  connection = pymysql.connect(host = '127.0.0.1',
        user = 'root',
        password = '',
        db = 'Calendar',
        charset = 'utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
  YicLogin(root, connection)
  root.mainloop()

if __name__ == '__main__':
  Main()
