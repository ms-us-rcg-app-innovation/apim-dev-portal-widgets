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
          <a v-if="products.length > 0" v-for="product in products" href="#" v-on:click.prevent="loadApis(product)">
            <div class="card item-tile">
              <h3>
                <span>{{ product.displayName }}</span>
              </h3>
              <div class="tile line-clamp">
                <p class="tile-content" v-html="product.description"></p>
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
      <h2>My APIs</h2>
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
        <div class="button-group-center">
          <a href="#" v-on:click.prevent="createProduct()" class="button">Create Product</a>
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
      selectedProduct: null as Product | null
    }
  },

  inject: ["secretsPromise", "requestPromise"],

  async mounted(): Promise<void> {

  },

  computed: {

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
    createProduct() {
      if (!this.selectedApis.length) {
        return;
      }

      var product = new Product();
      product.id = (parseInt(this.products[this.products.length - 1].id ?? "0") + 1).toString();
      product.displayName = "My Product";
      product.description = "<p>This is a custom Product made by the Consumer.</p>";
      
      for (let i = 0; i < this.selectedApis.length; i++) {
        product.apis.push(this.selectedApis[i]);
      }

      this.products.push(product);
      this.selectedApis = [];
      this.clearProduct();
    }
  },
}
</script>
