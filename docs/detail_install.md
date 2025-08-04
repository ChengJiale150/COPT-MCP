# 使用FastMCP快速一键配置

使用FastMCP配置该COPT-MCP是最快捷的配置方式,支持主流的客户端(如Claude Desktop/Claude Code/Cursor等一键配置),具体详见FastMCP官方文件的Integrations部分,例如[Claude Code配置COPT-MCP](https://gofastmcp.com/integrations/claude-code)

# 手动配置MCP服务

对于其他不支持FastMCP一键配置的应用(如TRAE,Cherry Studio等),可以使用手动配置对应的JSON格式,参考格式如下:

```json
"COPT-MCP": {
    "command": "uv",
    "args": [
    "run",
    "--with", "fastmcp",
    "--with", "requests",
    "--with", "sqlite_vec",
    "fastmcp", "run", 
    "your/path/to/COPT-MCP/server.py"
    ],
    "env": {},
    "transport": "stdio"
}
```

现在请按照如下步骤,进行相关配置:

## Step1: 确认你的文件地址

首先我们需要确认MCP服务器入口文件`server.py`的文件地址,用于替换上述参考配置中的`"your/path/to/COPT-MCP/server.py"`

### Windows 11

...

### MacOS

在`访达`中找到COPT-MCP对应的文件夹中的`server.py`文件,按下快捷键`option+command+c`复制文件路径,参考的路径如下:

```bash
/Users/username/Documents/mcp/copt-mcp/server.py
```

最后将上述参考JSON格式中的文件路径替换为复制完毕的路径,示例如下:

```json
"COPT-MCP": {
    "command": "uv",
    "args": [
    "run",
    "--with", "fastmcp",
    "--with", "requests",
    "--with", "sqlite_vec",
    "fastmcp", "run", 
    "/Users/username/Documents/mcp/copt-mcp/server.py"
    ],
    "env": {},
    "transport": "stdio"
}
```

## Step2: 设置必要的环境变量

注意,如果你在上述安装过程中已经在`config.json`中配置好对应的API Key,这步并非必要,直接跳过即可

如果按照下述步骤配置好API Key,也同样不需要配置`config.json`中对应的API Key

请在`env`中添加如下内容,注意这里的`API_KEY`为整个MCP所**共享**,不区分嵌入与重排序模型:

```json
"env":{
    "API_KEY" : "<your API Key>"
}
```

## Step3: 在对应客户端里添加MCP服务

接下来在对应客户端里的MCP配置文件中添加MCP服务即可

### Cursor

在Cursor右上角打开`Cursor Settings`(⚙图标),选择`Tool & Integrations`在`MCP Tools`中点击`New MCP Sever`就会跳转到`mcp.json`文件,呈现的示例结果如下:

```json
{
  "mcpServers": {
    ...(已有的MCP,若没有则为空)
  }
}
```

在已有的MCP后添加`,`(英文半角符号)(若无则无需添加),将之前已经填充完善好的JSON文件黏贴之后,最终的参考结果如下:

```json
{
  "mcpServers": {
    ...(已有的MCP,若没有则为空),
    "COPT-MCP" : {
        ...(上述具体内容)
    }
  }
}
```

最后保存并关闭`mcp.json`文件,返回查看`MCP Tools`中是否出现名为`COPT-MCP`的MCP服务,等待片刻,如果黄灯变绿灯则表明MCP服务启动成功

### Cherry Studio

在应用边侧打开设置按钮(⚙图标),选择`MCP设置`,点击`添加服务器`中的`从JSON导入`,输入如下内容:

```json
{
  "mcpServers": {
    "COPT-MCP" : {
        ...(上述具体内容)
    }
  }
}
```

点击确认,打开对应的MCP服务器,查看是否连接成功

### Trae

在应用边侧打开AI功能管理按钮(⚙图标),选择`MCP`,点击`手动添加`中的`从JSON导入`,输入如下内容:

```json
{
  "mcpServers": {
    "COPT-MCP" : {
        ...(上述具体内容)
    }
  }
}
```

点击确认,打开对应的MCP服务器,查看是否连接成功

## Step4: 测试MCP工具是否正常运行

接下来使用客户端支持MCP工具调用的模式(如Cursor中的Agent模式)测试MCP工具是否正常运行

### get_citation

测试输入: 

```
获取COPT在Word中的参考引用格式
```

期望输出: COPT的Word格式引用信息

### get_reference

测试输入: 

```
获取COPT在Python接口求解线性规划(LP)问题的参考范例
```

期望输出: COPT的Python接口LP问题的参考范例

### get_api_doc

测试输入: 

```
获取COPT中Python接口的矩阵形式添加线性约束的API接口信息
```

期望输出: Model.addMConstr()的相关API接口信息








