package auth

import (
	"fmt"
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/labstack/gommon/log"
	"go.opentelemetry.io/otel/trace"
)

type AuthController struct {
	service Service
	tracer  trace.Tracer
}

func NewAuthController(service Service, tracer trace.Tracer) AuthController {
	return AuthController{
		service: service,
		tracer:  tracer,
	}
}

func (controller *AuthController) Authenticate(c echo.Context) error {
	_, span := controller.tracer.Start(c.Request().Context(), "controller::Delete")
	defer span.End(trace.WithStackTrace(true))

	var user User
	if err := c.Bind(&user); err != nil {
		log.Error(err)
		return c.JSON(http.StatusBadRequest, "parsing error")
	}

	ids := []string{
		"1",
		"2",
		"3",
	}
	if len(user.Id) > 5 {
		fmt.Println(ids[len(ids)])
	}
	c.String(http.StatusOK, "Authenticated!")
	return nil
}
