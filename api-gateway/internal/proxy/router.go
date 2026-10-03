package proxy

import (
	"api-gateway/config"
	"net/http"
	"strings"
)

type Router struct {
	routes []config.Route
}

func NewRouter(routes []config.Route) *Router{
	return &Router{
		routes: routes,
	}
}

func matches ( routePath string, requestPath string) bool{
	if requestPath == routePath {
		return true
	}
	return strings.HasPrefix(requestPath,routePath+"/")
}

func (r *Router) Match(req *http.Request) (*config.Route,bool){
	for i := range r.routes {
		route := &r.routes[i]

		if matches(route.Path,req.URL.Path){
			return route,true
		}
	}
	return nil,false
}