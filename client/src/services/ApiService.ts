import { __Singleton } from "./__SingletonBase";

class ApiService extends __Singleton {
    constructor() {
        super();
    }
}

export default ApiService.getInstance();
