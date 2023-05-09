<style src="../../styles/app.scss"></style>

<template>
  <div v-if="true" class="height-fill">
    <div class="form-inline max-w-500">
      <p>Select a product to view APIs</p>
      <!-- <input type="search" class="form-control form-control-light" aria-label="Search" placeholder="Search products" spellcheck="false"
            data-bind="textInput: pattern" /> -->
    </div>

    <div style="clear:both"></div>

    <div class="column">
      <div class="cards" v-if="selectedProduct == null">
        <div class="cards-body" v-if="working">
          <!-- <spinner class="fit"></spinner> -->
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
                  <a href="#" v-on:click.prevent="editProduct(product)" class="button">Edit</a><br />
                  <a href="#" v-on:click.self="deleteProduct(product, index)" class="button">Delete</a>
                </p>
              </div>
            </div>
          </a>
          <p v-else>No products found</p>
        </div>
        <div class="cards-footer" v-if="!working && totalPages > 1">
          <!-- <pagination params="{ pageNumber: $component.pageNumber, totalPages: $component.totalPages }"></pagination> -->
        </div>
      </div>

      <div class="cards" v-if="selectedProduct != null">
        <div class="cards-body" v-if="working">
          <!-- <spinner class="fit"></spinner> -->
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

export default {
  data() {
    return {
      products: [
        {
          id: "1",
          displayName: "product 1",
          description: "<p>here's a <b>description</b><p>",
          isBase: true,
          apis: [{
            id: "1",
            name: "API 1",
          },
          {
            id: "2",
            name: "API 2",
          }]
        },
        {
          id: "2",
          displayName: "product 2",
          description: "<p>here's another <u>description</u><p>",
          isBase: true,
          apis: [{
            id: "3",
            name: "API 3",
          },
          {
            id: "4",
            name: "API 4",
          },
          {
            id: "5",
            name: "API 5",
          }]
        },
        {
          id: "3",
          displayName: "product 3",
          description: "<p>and again, another <i>description</i><p>",
          isBase: true,
          apis: [{
            id: "6",
            name: "API A",
          },
          {
            id: "7",
            name: "API B",
          },
          {
            id: "8",
            name: "API C",
          }]
        }
      ] as Product[],
      apis: [] as Api[],
      selectedApis: [] as Api[],
      working: false,
      pattern: "",
      pageNumber: 1,
      totalPages: 0,
      selectedProduct: null as Product | null,
      editingProduct: null as Product | null,
      productName: "" as string,
      productDescription: "" as string
    }
  },

  inject: ["secretsPromise", "requestPromise"],

  watch: {
    "selectedApis": function (val) {
      if (val && val.length && !this.editingProduct && this.productName == "" && this.productDescription == "") {
        this.productName = "My Product";
        this.productDescription = "This is a custom Product made by the Consumer";
      }
    }
  },

  methods: {
    loadApis(product: Product) {
      this.selectedProduct = product;
      this.apis = product.apis;
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
    createProduct() {
      if (!this.selectedApis.length) {
        return;
      }

      var product = new Product();
      product.id = (parseInt(this.products[this.products.length - 1].id ?? "0") + 1).toString();
      product.displayName = this.productName!;
      product.description = this.productDescription!;
      product.isBase = false;

      for (let i = 0; i < this.selectedApis.length; i++) {
        product.apis.push(this.selectedApis[i]);
      }

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

    saveProduct() {
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

      this.clear();
    },

    deleteProduct(product: Product, index: number) {
      this.products.splice(index, 1);
    }
  },
}
</script>
