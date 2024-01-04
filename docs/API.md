# API 文档

## User 模块
### login
实现通过微信账号的登录与注册功能
- **URL**：/user/login
- **方法**：POST
- **参数**：
  - code：用户的登录code，由前端调用`wx.login`获取
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - openid：仅成功时返回，用户的唯一`openid`

## Food 模块
### searchFood
搜索食物名称并返回匹配结果
- **URL**：/food/search
- **方法**：POST
- **参数**：
  - name：搜索字符串
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - results：仅成功时返回，匹配的搜索结果列表，列表中的每一项是一个字典，键值如下；如果没有匹配项，会返回空列表
    - name：食物名称
    - ms_unit：食物计量单位
    - purine_per_unit：食物每单位嘌呤含量
    - health_tip：食物健康提示
    - image_url：食物图片URL

### getFoodByName
根据食物名称返回食物的详细信息
- **URL**：/food/get
- **方法**：POST
- **参数**：
  - name：目标食物名称
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`；与搜索不同，当没有匹配项时结果为运行失败
  - message：仅失败时返回，描述错误原因
  - food：仅成功时返回，包含食物信息的字典，键值如下
    - name：食物名称
    - ms_unit：食物计量单位
    - purine_per_unit：食物每单位嘌呤含量
    - health_tip：食物健康提示
    - image_url：食物图片URL

## Record 模块
### addFoodRecord
添加饮食记录
- **URL**：/record/addFoodRecord
- **方法**：POST
- **参数**：
  - openid：添加记录用户的openid
  - food_name：食物名称
  - quantity：食物数量
  - record_date：记录日期（YYYY-MM-DD格式的字符串）
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - record_id：仅成功时返回，添加记录的id
  - message：仅失败时返回，描述错误原因

### addUricacidRecord
添加尿酸水平记录
- **URL**：/record/addUricacidRecord
- **方法**：POST
- **参数**：
  - openid：添加记录用户的openid
  - quantity：尿酸水平
  - record_date：记录日期（YYYY-MM-DD格式的字符串）
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - record_id：仅成功时返回，添加记录的id

### addFlareupRecord
添加痛风发作记录
- **URL**：/record/addFlareupRecord
- **方法**：POST
- **参数**：
  - openid：添加记录用户的openid
  - symptom：症状描述
  - intense_level：发作强度（1-5的整数）
  - trigger：诱因描述
  - record_date：记录日期（YYYY-MM-DD格式的字符串）
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - record_id：仅成功时返回，添加记录的id

### getFoodRecordsForDate
查询给定日期所有饮食记录
- **URL**：/record/recordForDate
- **方法**：POST
- **参数**：
  - openid：添加记录用户的openid
  - date：查询日期（YYYY-MM-DD格式的字符串）
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - records：仅成功时返回，描述给定日期的所有FoodRecord信息的列表，按创建时间排序；列表的每一项是一个字典，键值如下；如果查询日期没有记录，会返回空列表
    - food_name：该条记录的食物名称
    - ms_unit：食物的计量单位
    - image_url：食物图片URL
    - quantity：该条记录的食物数量
    - purine_content：该条记录的嘌呤摄入量
    - created_at：记录创建时间

### getFoodRecordSummary
查询以给定日期为基准，最近7天、30天、12月的饮食记录，计算统计量并返回，用于前端进行绘图
- **URL**：/record/foodRecordSummary
- **方法**：POST
- **参数**：
  - openid：添加记录用户的openid
  - reference_date：查询日期（YYYY-MM-DD格式的字符串）
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - summary：仅成功时返回，统计量字典
    - last_week：最近7天统计量；列表，每一项是一个字典，键值如下；前端应从索引1开始访问该列表
      - period：日期（YYYY-MM-DD格式的字符串）
      - total_purine：对应日期的嘌呤摄入量总和
    - last_month：最近30天统计量；格式同上
    - last_year：最近12月统计量；格式同上，但键值内容略有不同
      - period：日期（YYYY-MM格式的字符串）
      - total_purine：对应日期的嘌呤摄入量总和

### getUricacidSummary
查询以给定日期为基准，最近7天、30天、12月的尿酸记录，计算统计量并返回，用于前端进行绘图
- **URL**：/record/uricRecordSummary
- **方法**：POST
- **参数**：
  - openid：添加记录用户的openid
  - reference_date：查询日期（YYYY-MM-DD格式的字符串）
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - summary：仅成功时返回，统计量字典
    - last_week：最近7天统计量；列表，每一项是一个字典，键值如下；前端应从索引1开始访问该列表
      - period：日期（YYYY-MM-DD格式的字符串）
      - average_quantity：对应日期的尿酸水平平均值
    - last_month：最近30天统计量；格式同上
    - last_year：最近12月统计量；格式同上，但键值内容略有不同
      - period：日期（YYYY-MM格式的字符串）
      - average_quantity：对应日期的尿酸水平平均值

### getFlareupSummary
查询以给定日期为基准，最近7天、30天、12月的尿酸记录，计算统计量并返回，用于前端进行绘图
- **URL**：/record/flareRecordSummary
- **方法**：POST
- **参数**：
  - openid：添加记录用户的openid
  - reference_date：查询日期（YYYY-MM-DD格式的字符串）
- **响应**：
  - status：运行结果，可能为`"success"`或`"error"`
  - message：仅失败时返回，描述错误原因
  - summary：仅成功时返回，统计量字典
    - last_week：最近7天统计量；列表，每一项是一个字典，键值如下；前端应从索引1开始访问该列表
      - period：日期（YYYY-MM-DD格式的字符串）
      - average_intensity：对应日期的发作强度平均值
    - last_month：最近30天统计量；格式同上
    - last_year：最近12月统计量；格式同上，但键值内容略有不同
      - period：日期（YYYY-MM格式的字符串）
      - average_quantity：对应日期的发作强度平均值