package hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class Application {

    @RequestMapping("/")
    public String home() {
        return "Hello Docker World";
    }
    
    @RequestMapping("/about")
    public String about() {
        return "Hello about service";
    }
    
    @RequestMapping("/help")
    public String help() {
        return "Help Service";
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
