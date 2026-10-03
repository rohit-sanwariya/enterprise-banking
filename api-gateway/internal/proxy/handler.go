package proxy

import (
	"log"
	"net/http"
)

type Handler struct {
	router  *Router
	proxies map[string]http.Handler
}

func NewHandler(router *Router, proxies map[string]http.Handler) *Handler {
	return &Handler{
		router:  router,
		proxies: proxies,
	}
}

func (p *Proxy) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	p.proxy.ServeHTTP(w, r)
}
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	route, ok := h.router.Match(r)
	if !ok {
		http.NotFound(w, r)
	}

	proxy, ok := h.proxies[route.Service]
	if !ok {
		http.Error(w, "Service unavailable", http.StatusBadGateway)
		return
	}
	log.Print("service routed", route.Service)
	proxy.ServeHTTP(w, r)
}
