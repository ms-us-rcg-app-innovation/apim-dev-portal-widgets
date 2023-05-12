import { RequestBase } from "./requestBase"

export class GetProductsRequest extends RequestBase {
    public baseProductTag: string;

    constructor(sasToken: string, baseProductTag: string) {
        super(sasToken);
        this.baseProductTag = baseProductTag;
    }

    get path() {
        return `/list_tagged_products?token=${this.sasToken}&tagIds=${this.baseProductTag}`
    } 
}