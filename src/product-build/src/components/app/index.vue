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
        <a v-if="products.length > 0" v-for="product in products" href="#" v-on:click="selectedProduct = product">
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
        <a href="#" v-on:click="selectedProduct = null">Back to Products</a>
        <!-- <a v-if="products.length > 0" v-for="product in products" href="#">
          <div class="card item-tile">
            <h3>
              <span>{{ product.title }}</span>
            </h3>
            <div class="tile line-clamp">
              <p class="tile-content" v-html="product.description"></p>
            </div>
          </div>
        </a>
        <p v-else>No products found</p> -->
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
      working: false,
      pattern: "",
      pageNumber: 1,
      totalPages: 0,
      selectedProduct: null as Product | null
    }
  },

  inject: ["secretsPromise", "requestPromise"],

  async mounted(): Promise<void> {
    const editorData = getValues(valuesDefault);

    const [secrets, request] = await Promise.all([this.secretsPromise, this.requestPromise]);

    if (!secrets.userId) {
      return;
    }
  }
}
</script>
