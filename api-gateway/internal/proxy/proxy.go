package proxy

import (
	"api-gateway/config"
	"net/http/httputil"
	"net/url"
)

type Proxy struct {
	target *url.URL
	proxy  *httputil.ReverseProxy
}

func NewProxy(service config.Service) (*Proxy,error) {
	target , err := url.Parse(service.URL)
	if err != nil {
		return nil,err
	}

	return &Proxy{
		target: target,
		proxy: httputil.NewSingleHostReverseProxy(target),
	},nil
}


