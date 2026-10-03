package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

func LoadRoutes(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read route config: %w", err)
	}

	var config Config

	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("parse route config: %w", err)
	}

	if err := validate(config); err != nil {
		return nil, err
	}

	return &config, nil
}

func validate(config Config) error {
	if len(config.Routes) == 0 {
		return fmt.Errorf("route config contains no routes")
	}

	for i, route := range config.Routes {
		if route.Path == "" {
			return fmt.Errorf("route[%d]: path is required", i)
		}

		if route.Service == "" {
			return fmt.Errorf("route[%d]: service is required", i)
		}

		service, exists := config.Services[route.Service]
		if !exists {
			return fmt.Errorf(
				"route[%d]: unknown service %q",
				i,
				route.Service,
			)
		}

		if service.URL == "" {
			return fmt.Errorf(
				"route[%d]: service %q has empty URL",
				i,
				route.Service,
			)
		}
	}

	return nil
}
