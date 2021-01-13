import discord
from discord.ext import commands
import asyncio
import call_flask
import makepretty
from datetime import datetime
import os




CLIENT_SECRET = os.environ['CLIENT_SECRET']
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(pass_context=True, brief='responds, for testing')
async def ping(ctx):
    await ctx.send('pong')

@bot.command(pass_context=True, brief='gets todos <view>')
async def gettodos(ctx, view='all'):
    if view == 'all':
        json = call_flask.get_todos()
        await ctx.send(makepretty.todo_json_to_string(json, view=view))
    elif view in ['completed','complete','1']:
        view = 'completed'
        json = call_flask.get_todos()
        await ctx.send(makepretty.todo_json_to_string(json, view=view))
    elif view in ['incompleted', 'incomplete','0']:
        view = 'incompleted'
        json = call_flask.get_todos()
        await ctx.send(makepretty.todo_json_to_string(json, view=view))
    else:
        await ctx.send('Request invalid. Please refer to help.')

@bot.command(pass_context=True, brief='adds a todo <user ... user> <text>')
async def addtodo(ctx, *args):
    if args[0].startswith('<@'):
        post_text = ''
        dependent_users = []
        for arg in args:
            if arg.startswith('<@'):
                dependent_users.append(arg)
            else:
                post_text += arg + ' '

        print(post_text,dependent_users)
        await ctx.send(makepretty.todo_post_response_to_string(call_flask.post_todo(text=post_text, dependent_users=dependent_users)))
    else:
        await ctx.send('Request invalid. Please refer to help.')


@bot.command(pass_context=True, brief='updates todo completion <todo_id> <complete>')
async def completetodo(ctx, todo_id, completed):
    try:
        if completed in ['true', 'True', '1', 'complete', 'completed']:
            completed = True
            print(todo_id, completed)
            await ctx.send(makepretty.todo_put_response_to_string(call_flask.put_todo(todo_id, completed=completed)))
        elif completed in ['false', 'False', '0', 'incomplete', 'incompleted']:
            completed = False
            print(todo_id, completed)
            await ctx.send(makepretty.todo_put_response_to_string(call_flask.put_todo(todo_id, completed)))
        else:
            await ctx.send('Request invalid: <completed> is true or false?')
    except Exception as e:
        await ctx.send('Request invalid: ' + str(e))

@bot.command(pass_context=True, breif='edits the text of a todo <text>')
async def edittodo(ctx, *args):
    text = ''
    todo_id = args[0]
    del args[0]
    for arg in args:
        text += arg + ' '
    print(todo_id, text)
    await ctx.send(makepretty.todo_put_response_to_string(call_flask.put_todo(todo_id, text=text)))

@bot.command(pass_context=True, brief='gets todos with mentions')
async def pingtodos(ctx):
    json = call_flask.get_todos()
    await ctx.send(makepretty.todo_json_to_string_with_mentions(json))

@bot.command(pass_context=True, brief='deletes a todo <todo_id>')
async def deltodo(ctx, todo_id):
    await ctx.send(makepretty.todo_delete_response_to_string(call_flask.delete_todo(todo_id)))

@bot.command(pass_context=True, brief='gives grippos')
async def grippos(ctx):
    await ctx.send('I am running out of bags ... :pensive:')
    await ctx.send(file=discord.File('img_grippos.png'))

async def ping_todos():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            channel = bot.get_channel(784616083835060255)
            now = datetime.now()
            print('Checking if it is 8:00...')
            if (now.hour == 8 or now.hour == 20) and (now.minute == 0):
                print('It is 8. Sending...')
                await channel.send(makepretty.todo_json_to_string_with_mentions(call_flask.get_todos()))
            else:
                print('It is not 8.')
            await asyncio.sleep(delay=60)
            
        except Exception as e:
            print(e)



bot.loop.create_task(ping_todos())
bot.run(CLIENT_SECRET)