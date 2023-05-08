<style src="../../styles/app.scss"></style>

<template>
  <div v-if="true" class="flex-columns-container height-fill">
    <div class="form-inline max-w-500">
      <p>Select a product to view APIs</p>
      <!-- <input type="search" class="form-control form-control-light" aria-label="Search" placeholder="Search products" spellcheck="false"
            data-bind="textInput: pattern" /> -->
    </div>

    <div class="cards" v-if="selectedProduct == null">

      <div class="cards-body" v-if="working">
        <!-- <spinner class="fit"></spinner> -->
        working...
      </div>
      <div class="cards-body animation-fade-in" v-else>
        <h4>Products</h4>
        <a v-if="products.length > 0" v-for="product in products" href="#" v-on:click="loadApis(product)">
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

      <div class="cards-body animation-fade-in">
        <h4>{{ selectedProduct.displayName }} APIs</h4>
        <ul v-if="apis.length">
          <li v-for="api in apis">
            <input type="checkbox" v-model="api.selected" /> {{ api.name }}
          </li>
        </ul>
        <a href="#" v-on:click="addSelectedApis()">Add to My APIs</a><br/>
        <a href="#" v-on:click="clearProduct()">Back to Products</a>
      </div>
    </div>

    <div class="cards" >
      <p>My APIs</p>
      <div v-if="selectedApis.length">
        <ul v-if="selectedApis.length">
          <li v-for="(api, index) in selectedApis">
            {{ api.name }}&nbsp;<a href="#" v-on:click="removeSelectedApi(index)">Remove</a>
          </li>
        </ul>
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
          description: "<p>here's a <b>description</b><p>"
        },
        {
          id: "2",
          displayName: "product 2",
          description: "<p>here's another <u>description</u><p>"
        },
        {
          id: "3",
          displayName: "product 3",
          description: "<p>and again, another <i>description</i><p>"
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
    // const editorData = getValues(valuesDefault);

    // const [secrets, request] = await Promise.all([this.secretsPromise, this.requestPromise]);

    // if (!secrets.userId) {
    //   return;
    // }
  },

  computed:{

  },

  methods: {
    loadApis(product: Product) {
      const dummyAPIs = [{
        id: "1",
        name: "API 1",
      },
      {
        id: "2",
        name: "API 2",
      },
      {
        id: "3",
        name: "API 3",
      },
      {
        id: "4",
        name: "API 4",
      },] as Api[]

      this.selectedProduct = product;
      this.apis = dummyAPIs;
    },
    clearProduct() {
      this.selectedProduct = null;
      this.apis = [];
    },
    addSelectedApis() {
      var selectedApis = this.apis.filter(api => api.selected);

      if (!selectedApis.length) {
        return
      }

      for (let i = 0; i < selectedApis.length; i++) {
        this.selectedApis.push(selectedApis[i])
      }

      this.clearProduct();
    },
    removeSelectedApi(index: number) {
      this.selectedApis.splice(index, 1);
    }
  },
}
</script>
