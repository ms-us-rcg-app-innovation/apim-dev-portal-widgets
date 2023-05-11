<style src="../../styles/app.scss"></style>

<template>
  <div v-if="true" class="height-fill">
    <div class="form-inline max-w-500">
      <p>Select a Product to view APIs. Select one or more APIs to build a Product.</p>
    </div>

    <div style="clear:both"></div>

    <div class="column">
      <div class="cards" v-if="selectedProduct == null">
        <div class="cards-body" v-if="working">
          working...
        </div>
        <div class="cards-body animation-fade-in" v-else>
          <h2>Products</h2>
          <a v-if="products.length > 0" v-for="(product, index) in products">
            <div class="card item-tile">
              <h3 style="cursor: pointer;" v-on:click.prevent="loadApis(product)">
                <span>{{ product.displayName }}</span>
              </h3>
              <div class="tile line-clamp">
                <p class="tile-content" v-html="product.description"></p>
                <p v-if="!product.isBase && editingProduct == null">
                  <a href="#" v-on:click.prevent="editProduct(product)" class="button">Edit</a>&nbsp;
                  <a href="#" v-on:click.self="deleteProduct(product, index)" class="button">Delete</a>
                </p>
              </div>
            </div>
          </a>
          <p v-else>No products found</p>
        </div>
      </div>

      <div class="cards" v-if="selectedProduct != null">
        <div class="cards-body" v-if="working">
          working...
        </div>
        <div class="cards-body animation-fade-in" v-else>
          <h2>{{ selectedProduct.displayName }} APIs</h2>
          <div v-if="apis.length > 0">
            <div v-for="api in apis">
              <div class="card item-tile">
                <h3>
                  <span>{{ api.name }}</span>
                </h3>
                <div class="tile line-clamp">
                  <p class="tile-content" v-html="api.description"></p>
                  <p><a href="#" v-on:click.prevent="addApiToProduct(api)" class="button">Add to My Product</a></p>
                </div>
              </div>
            </div>
            <div class="button-group-center">
              <a href="#" v-on:click.prevent="clearProduct()" class="button">Back to Products</a>
            </div>
          </div>
          <div v-else>
            <p>No APIs found</p>
          </div>
        </div>
      </div>
    </div>

    <div class="column">
      <h2 v-if="editingProduct">{{ editingProduct.displayName }} APIs</h2>
      <h2 v-else>New Product APIs</h2>
      <div v-if="selectedApis.length">
        <div v-for="(api, index) in selectedApis">
          <div class="card item-tile">
            <h3>
              <span>{{ api.name }}</span>
            </h3>
            <div class="tile line-clamp">
              <p><a href="#" v-on:click.prevent="removeSelectedApi(index)" class="button">Remove</a></p>
            </div>
          </div>
        </div>
        <div class="form">
          <div class="form-group">
            <label for="product-edit-name" class="form-label">Name</label>
            <input id="product-edit-name" type="text" class="form-control" v-model="productName" />
          </div>
          <div class="form-group">
            <label for="product-edit-desc" class="form-label">Description</label>
            <input id="product-edit-desc" type="text" class="form-control" v-model="productDescription" />
          </div>
        </div>
        <div v-if="editingProduct" class="button-group-center">
          <a href="#" v-on:click.prevent="saveProduct()" class="button">Save Product</a>
          <a href="#" v-on:click.prevent="clear()" class="button">Cancel</a>
        </div>
        <div v-else class="button-group-center">
          <a href="#" v-on:click.prevent="createProduct()" class="button">Create Product</a>
          <a href="#" v-on:click.prevent="clear()" class="button">Cancel</a>
        </div>
      </div>
      <div v-else>
        <p>No APIs selected.</p>
      </div>
    </div>
  </div>
  <div v-else class="loading">
    loading...
  </div>
</template>

<script lang="ts">
import { getValues } from "@azure/api-management-custom-widgets-tools"
import { valuesDefault } from "../../values"
import { Product } from "../../models/product";
import { Api } from "../../models/api";
import { ProductService } from "../../models/productService";

export default {
  data() {
    return {
      products: [] as Product[],
      apis: [] as Api[],
      selectedApis: [] as Api[],
      working: false,
      pattern: "",
      pageNumber: 1,
      totalPages: 0,
      selectedProduct: null as Product | null,
      editingProduct: null as Product | null,
      productName: "" as string,
      productDescription: "" as string,
      accessToken: "" as string,
      endpoint: ""
    }
  },

  inject: ["secretsPromise"],

  watch: {
    "selectedApis": function (val) {
      if (val && val.length && !this.editingProduct && this.productName == "" && this.productDescription == "") {
        this.productName = "My Product";
        this.productDescription = "This is a custom Product made by the Consumer";
      }
    }
  },

  async mounted(): Promise<void> {
    const secrets = await this.secretsPromise;
    this.accessToken = secrets.token; // SAS token
    await this.loadProducts();
  },

  methods: {
    async loadProducts(): Promise<void> {
      let productService = new ProductService(this.endpoint, this.accessToken);
      var response = await productService.getList();
      this.products = response.products ?? [];
    },
    async loadApis(product: Product): Promise<void> {
      let productService = new ProductService(this.endpoint, this.accessToken);
      var response = await productService.getApis(product.id!);

      this.selectedProduct = product;
      this.apis = response.apis ?? [];
    },
    clearProduct() {
      this.selectedProduct = null;
      this.apis = [];
    },
    addApiToProduct(api: Api) {
      this.selectedApis.push(api);
    },
    removeSelectedApi(index: number) {
      this.selectedApis.splice(index, 1);
    },
    clear() {
      this.selectedApis = [];
      this.editingProduct = null;
      this.productName = "";
      this.productDescription = "";
      this.clearProduct();
    },
    async createProduct() : Promise<void> {
      if (!this.selectedApis.length) {
        return;
      }

      var product = new Product();
      product.displayName = this.productName!;
      product.description = this.productDescription!;
      product.isBase = false;

      for (let i = 0; i < this.selectedApis.length; i++) {
        product.apis.push(this.selectedApis[i]);
      }

      let productService = new ProductService(this.endpoint, this.accessToken);
      var response = await productService.saveProduct(product);

      if (!response.product) {
        throw new Error("Product not returned.");
      }
      product.id = response.product.id;

      this.products.push(product);
      this.clear();
    },
    editProduct(product: Product) {
      this.editingProduct = product;
      this.productName = product.displayName!;
      this.productDescription = product.description!;
      this.selectedApis = [];

      for (let i = 0; i < product.apis.length; i++) {
        this.selectedApis.push(product.apis[i]);
      }
    },

    async saveProduct(): Promise<void> {
      if (!this.editingProduct) {
        return;
      }

      if (!this.selectedApis.length) {
        return;
      }

      var product = this.editingProduct;
      product.apis = [];

      for (let i = 0; i < this.selectedApis.length; i++) {
        product.apis.push(this.selectedApis[i]);
      }

      let productService = new ProductService(this.endpoint, this.accessToken);
      await productService.saveProduct(product);

      this.clear();
    },

    async deleteProduct(product: Product, index: number) : Promise<void> {
      let productService = new ProductService(this.endpoint, this.accessToken);
      await productService.deleteProduct(product.id!)

      this.products.splice(index, 1);
    }
  },
}
</script>
