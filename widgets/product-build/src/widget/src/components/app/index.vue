<style src="../../styles/app.scss"></style>

<template>
  <div v-if="!loading" class="height-fill">
    <div class="form-inline max-w-500">
    <input type="search" class="form-control form-control-light" aria-label="Search" placeholder="Search products" spellcheck="false" v-model="searchPattern" />
      <p>Select a Product to view APIs. Select one or more APIs to build a Product.</p>
    </div>

    <div style="clear:both"></div>

    <div class="column">
      <div class="cards" v-if="selectedProduct == null">
        <div class="cards-body animation-fade-in">
          <h2>Products</h2>
          <a v-if="filteredProducts.length > 0" v-for="product in filteredProducts">
            <div class="card item-tile">
              <h3 style="cursor: pointer;" v-on:click.prevent="loadApis(product)">
                <span>{{ product.displayName }}</span>
              </h3>
              <div class="tile line-clamp">
                <p class="tile-content" v-html="product.description"></p>
                <p v-if="!product.isBase">
                  <a href="#" v-on:click.self="deleteProduct(product)" class="button button-delete button-small">Delete</a>
                </p>
              </div>
            </div>
          </a>
          <p v-else>No products found.</p>
        </div>
      </div>

      <div class="cards" v-if="selectedProduct != null">
        <div class="cards-body animation-fade-in">
          <h2>{{ selectedProduct.displayName }}</h2>
          <h3>APIs</h3>
          <div v-if="apis.length > 0">
            <div v-for="api in apis">
              <div class="card item-tile">
                <h3>
                  <span>{{ api.name }}</span>
                </h3>
                <div class="tile line-clamp">
                  <p class="tile-content" v-html="api.description"></p>
                  <p><a href="#" v-on:click.prevent="addApiToProduct(api)" class="button button-small">Add to My Product</a></p>
                </div>
              </div>
            </div>
            <div v-if="subscriptionKeysEnabled">
              <a href="#" v-on:click.prevent="showSubscriptionKeys = !showSubscriptionKeys">{{ showSubscriptionKeys ? "Hide Subscription Keys" : "Show Subscription Keys" }}</a>
            </div>
            <div v-if="subscriptionKeysEnabled && showSubscriptionKeys" class="form">
              <h3>Subscription Keys</h3>
              <div class="form-group">
                <label for="subscription-primary-key" class="form-label">Primary Key</label>
                <input id="subscription-primary-key" type="text" class="form-control" v-model="selectedProduct.subscriptionKeys[0]"/>
              </div>
              <div class="form-group">
                <label for="subscription-secondary-key" class="form-label">Secondary Key</label>
                <input id="subscription-secondary-key" type="text" class="form-control" v-model="selectedProduct.subscriptionKeys[1]"/>
              </div>
            </div>
            <div class="button-group-center">
              <a href="#" v-on:click.prevent="clearProduct()" class="button button-small button-cancel">Back to Products</a>
            </div>
          </div>
          <div v-else>
            <p>No APIs found.</p>
          </div>

        </div>
      </div>
    </div>

    <div class="column">
      <h2>New Product APIs</h2>
      <div v-if="selectedApis.length">
        <div v-for="(api, index) in selectedApis">
          <div class="card item-tile">
            <h3>
              <span>{{ api.name }}</span>
            </h3>
            <div class="tile line-clamp">
              <p><a href="#" v-on:click.prevent="removeSelectedApi(index)" class="button button-small button-delete">Remove</a></p>
            </div>
          </div>
        </div>
        <!-- <div class="form">
          <div class="form-group">
            <label for="product-edit-name" class="form-label">Name</label>
            <input id="product-edit-name" type="text" class="form-control" v-model="productName" />
          </div>
          <div class="form-group">
            <label for="product-edit-desc" class="form-label">Description</label>
            <input id="product-edit-desc" type="text" class="form-control" v-model="productDescription" />
          </div>
        </div> -->
        <div class="button-group-center">
          <a href="#" v-on:click.prevent="createProduct()" class="button button-small">Create Product</a>
          <a href="#" v-on:click.prevent="clear()" class="button button-cancel button-small">Cancel</a>
        </div>
      </div>
      <div v-else>
        <p>No APIs selected.</p>
      </div>
    </div>
  </div>
  <div v-else>
    <Spinner />
  </div>
</template>

<script lang="ts">
import { getValues } from "@azure/api-management-custom-widgets-tools"
import { Values, valuesDefault } from "../../values"
import { Product } from "../../models/product";
import { Api } from "../../models/api";
import { ProductService } from "../../models/productService";
import Spinner from "../spinner/index.vue"

export default {
  components: {
    Spinner
  },

  data() {
    return {
      products: [] as Product[],
      apis: [] as Api[],
      selectedApis: [] as Api[],
      searchPattern: "" as String,
      loading: false,
      selectedProduct: null as Product | null,
      showSubscriptionKeys: false,
      productName: "" as string,
      productDescription: "" as string,
      settings: {} as Values,
      accessToken: "" as string,
      userId: "" as string,
    }
  },

  inject: ["secretsPromise"],

  watch: {
    "selectedApis": function (val) {
      if (val && val.length && this.productName == "" && this.productDescription == "") {
        this.productName = this.settings.productNamePlaceholder;
        this.productDescription = this.settings.productDescriptionPlaceholder;
      }
    }
  },

  async mounted(): Promise<void> {
    const editorData = getValues(valuesDefault);

    this.settings.endpoint = editorData.endpoint;
    this.settings.baseProductTag = editorData.baseProductTag;
    this.settings.productDescriptionPlaceholder = editorData.productDescriptionPlaceholder;
    this.settings.productNamePlaceholder = editorData.productNamePlaceholder;
    this.settings.debugModeEnabled = editorData.debugModeEnabled;

    const secrets = await this.secretsPromise;
    this.accessToken = secrets.token; // SAS token
    this.userId = secrets.userId;

    if (this.settings.debugModeEnabled) {
      console.log("sas_token", this.accessToken);
      console.log("userId", this.userId);
    }

    await this.loadProducts();
  },

  computed: {
    filteredProducts(): Product[]  {
      let pattern = (this.searchPattern as string)?.toLowerCase();
      if (!pattern) {
        return this.products;
      }

      return this.products.filter(p => p.displayName?.toLowerCase().includes(pattern) || p.description?.toLowerCase().includes(pattern));
    },
    subscriptionKeysEnabled(): boolean {
      return this.selectedProduct != null && !this.selectedProduct.isBase 
          && this.selectedProduct.subscriptionKeys && this.selectedProduct.subscriptionKeys.length > 0;
    }
  },

  methods: {
    getProductService() {
      return new ProductService(this.settings.endpoint, this.accessToken, this.settings.baseProductTag);
    },
    async loadProducts(): Promise<void> {
      try {
        this.loading = true;
        var response = await this.getProductService().getList();
        this.products = response.products ?? [];
      } finally {
        this.loading = false;
      }
    },
    async loadApis(product: Product): Promise<void> {
      try {
        this.loading = true;
        var response = await this.getProductService().getApis(product.id!);

        this.selectedProduct = product;
        this.selectedProduct.subscriptionKeys = response.keys ?? [];
        this.apis = response.apis ?? [];
      } finally {
        this.loading = false;
      }
      
    },
    clearProduct() {
      this.selectedProduct = null;
      this.showSubscriptionKeys = false;
      this.apis = [];
    },
    addApiToProduct(api: Api) {
      if (!this.selectedApis.some(item => item.id == api.id)) {
        this.selectedApis.push(api);
      } else {
        alert("This API is already a part of the Product. Please select another API.");
      }
    },
    removeSelectedApi(index: number) {
      this.selectedApis.splice(index, 1);
    },
    clear() {
      this.selectedApis = [];
      this.productName = "";
      this.productDescription = "";
      this.clearProduct();
    },
    async refresh() : Promise<void> {
      this.clear();
      await this.loadProducts();
    },
    async createProduct() : Promise<void> {
      if (!this.selectedApis.length) {
        return;
      }

      var product = new Product();
      product.displayName = this.productName!;
      product.description = this.productDescription!;
      product.isBase = false;
      product.setApiIds(this.selectedApis);

      try {
        this.loading = true;
        await this.getProductService().saveProduct(product);
      } finally {
        this.loading = false;
      }
     
      await this.refresh();
    },
    async deleteProduct(product: Product) : Promise<void> {
      if (!confirm("Are you sure you want to delete this Product?")) {
        return;
      }

      try {
        this.loading = true;
        await this.getProductService().deleteProduct(product.id!)
      } finally {
        this.loading = false;
      }

      await this.refresh();
    }
  },
}
</script>
