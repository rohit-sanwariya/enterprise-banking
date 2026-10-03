package config

type Config struct {
	Services map[string]Service `yaml:"services"`
	Routes   []Route            `yaml:"routes"`
}

type Service struct {
	URL string `yaml:"url"`
}

type Route struct {
	Path    string `yaml:"path"`
	Service string `yaml:"service"`
}
