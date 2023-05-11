import { GetProductsRequest } from "./getProductsRequest"
import { GetProductsResponse } from "./getProductsResponse"
import { GetApisRequest } from "./getApisRequest"
import { GetApisResponse } from "./getApisResponse"
import { Product } from "./product"
import { SaveProductRequest } from "./saveProductRequest"
import { SaveProductResponse } from "./saveProductResponse"
import { DeleteProductRequest } from "./deleteProductRequest"

export class ProductService {
    private endpoint: string;
    private baseProductTag: string;
    private sasToken: string;

    constructor(endpoint: string, sasToken: string, baseProductTag?: string) {
        this.endpoint = endpoint;
        this.sasToken = sasToken;
        this.baseProductTag = baseProductTag ?? "base-product";
    }

    public async getList(): Promise<GetProductsResponse> {
        let request = new GetProductsRequest(this.sasToken, this.baseProductTag);

        let response = await fetch(`${this.endpoint}/products`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error("Failed to get list of Products");
        }

        let responseJson: GetProductsResponse = await response.json();
        return responseJson;
    }

    public async getApis(productId: string): Promise<GetApisResponse> {
        let request = new GetApisRequest(this.sasToken, productId);

        let response = await fetch(`${this.endpoint}/apis`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error("Failed to get list of Apis");
        }

        let responseJson: GetApisResponse = await response.json();
        return responseJson;
    }

    public async saveProduct(product: Product): Promise<SaveProductResponse> {
        let request = new SaveProductRequest(this.sasToken, product);

        let response = await fetch(`${this.endpoint}/product`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error("Failed to get list of Apis");
        }

        let responseJson: SaveProductResponse = await response.json();
        return responseJson;
    }

    public async deleteProduct(productId: string): Promise<void> {
        let request = new DeleteProductRequest(this.sasToken, productId);

        let response = await fetch(`${this.endpoint}/product`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error("Failed to get list of Apis");
        }
    }

}