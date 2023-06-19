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

    constructor(endpoint: string, sasToken: string, baseProductTag: string) {
        this.endpoint = endpoint;
        this.sasToken = sasToken;
        this.baseProductTag = baseProductTag;
    }

    public async getList(): Promise<GetProductsResponse> {
        let baseProductsRequest = new GetProductsRequest(this.sasToken, this.baseProductTag);
        let userProductsRequest = new GetProductsRequest(this.sasToken);

        let baseProductResponse = await this.getListInternal(baseProductsRequest);
        let userProductsResponse = await this.getListInternal(userProductsRequest);

        if (baseProductResponse.products) {
            for (let i = 0; i < baseProductResponse.products.length; i++) {
                baseProductResponse.products[i].isBase = true;
            }
        }
       
        let productResponse =  new GetProductsResponse();
        productResponse.products = baseProductResponse.products?.concat(userProductsResponse.products ?? []);

        return productResponse;
    }

    private async getListInternal(request: GetProductsRequest) : Promise<GetProductsResponse> {
        let response = await fetch(`${this.endpoint}${request.path}`, {
            method: "GET",
            headers: request.headers
        });

        if (!response.ok) {
            throw new Error("Failed to get list of Products.");
        }

        let responseProductJson: Product[] = await response.json();

        for (let i = 0; i < responseProductJson.length; i++) {
            if (!responseProductJson[i].displayName && responseProductJson[i].name) {
                responseProductJson[i].displayName = responseProductJson[i].name;
            }
        }

        let productResponse =  new GetProductsResponse();
        productResponse.products = responseProductJson;

        return productResponse;
    }

    public async getApis(productId: string): Promise<GetApisResponse> {
        let request = new GetApisRequest(this.sasToken, productId);

        let response = await fetch(`${this.endpoint}${request.path}`, {
            method: "GET",
            headers: request.headers
        });

        if (!response.ok) {
            throw new Error("Failed to get list of APIs.");
        }

        let responseApiJson: GetApisResponse = await response.json();

        if (responseApiJson.apis) {
            for (let i = 0; i < responseApiJson.apis?.length; i++) {
                if (!responseApiJson.apis[i].displayName && responseApiJson.apis[i].name) {
                    responseApiJson.apis[i].displayName = responseApiJson.apis[i].name;
                }
            }
        }

        return responseApiJson;
    }

    public async saveProduct(product: Product): Promise<SaveProductResponse> {
        let request = new SaveProductRequest(this.sasToken, product);

        let response = await fetch(`${this.endpoint}${request.path}`, {
            method: "POST",
            headers: request.headers,
            body: request.body
        });

        if (!response.ok) {
            throw new Error("Failed to save Product.");
        }

        let responseJson: SaveProductResponse = await response.json();
        return responseJson;
    }

    public async deleteProduct(productId: string): Promise<void> {
        let request = new DeleteProductRequest(this.sasToken, productId);

        let response = await fetch(`${this.endpoint}${request.path}`, {
            method: "DELETE",
            headers: request.headers
        });

        if (!response.ok) {
            throw new Error("Failed to delete Product.");
        }
    }
}