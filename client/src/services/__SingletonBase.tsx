export class __Singleton {
    private static instances: Map<string, any> = new Map();

    public constructor() {
        // Prevent external instantiation
    }

    public static getInstance<T extends typeof __Singleton>(this: T): InstanceType<T> {
        // Use 'this' to refer to the calling class, supporting inheritance
        if (!__Singleton.instances.has(this.name)) {
            __Singleton.instances.set(this.name, new this());
        }
        return __Singleton.instances.get(this.name);
    }
}
