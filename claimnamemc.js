const fs = require('fs')
const mineflayer = require('mineflayer')
const opn = require('opn')

const namesniped = fs.readFileSync('nametoclaim.txt', 'utf8').trim().split('/')
const username = namesniped[0]
const password = namesniped[1]

const bot = mineflayer.createBot({
  host: 'blockmania.com',
  port: 25565,
  version: '1.14.2',
  username: username,
  password: password,
  auth: 'microsoft'
})



bot.once('spawn', () => {
  
  setTimeout(() => {
    bot.chat('/namemc')
  }, 3000)
  
})

bot.on('message', (message) => {
  if (message.toString().includes('https://namemc.com/claim?key=')) {
    const match = message.toString().match(/https:\/\/namemc\.com\/claim\?key=[^\s]+/)
    if (match) {
      const link = match[0]
      
      opn(link)
      bot.quit()
    }
  }
})
