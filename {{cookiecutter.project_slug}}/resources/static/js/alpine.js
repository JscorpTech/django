import Alpine from 'alpinejs'
import counter from "./counter";

window.Alpine = Alpine

Alpine.data("vars", counter)

Alpine.start()

