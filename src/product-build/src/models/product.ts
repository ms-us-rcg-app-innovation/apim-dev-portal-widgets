import { Api } from "./api"
export class Product {
    public id?: string;
    public name?: string;
    public displayName?: string;
    public description?: string;

    public apiIds: string = "";
    public isBase: boolean = true;

    public setApiIds(apis: Api[])
    {
        this.apiIds = apis.map(api => api.id).join(",")
    }
}