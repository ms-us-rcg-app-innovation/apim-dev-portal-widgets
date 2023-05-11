<style lang="scss" src="../../styles/editor.scss"></style>

<template>
    <div class="form">
    <div class="form-group">
      <label for="productNamePlaceholder" class="form-label">Product Name Placeholder</label>
      <input id="productNamePlaceholder" type="text" class="form-control" v-model="productNamePlaceholder" :placeholder="valuesDefault.productNamePlaceholder" />
    </div>
    <div class="form-group">
      <label for="productDescPlaceholder" class="form-label">Product Desc Placeholder</label>
      <input id="productDescPlaceholder" type="text" class="form-control" v-model="productDescriptionPlaceholder" :placeholder="valuesDefault.productDescriptionPlaceholder" />
    </div>
    <div class="form-group">
      <label for="endpoint" class="form-label">Endpoint</label>
      <input id="endpoint" type="text" class="form-control" v-model="endpoint" :placeholder="valuesDefault.endpoint" />
    </div>
    <div class="form-group">
      <label for="baseProductTag" class="form-label">Base Product Tag</label>
      <input id="baseProductTag" type="text" class="form-control" v-model="baseProductTag" :placeholder="valuesDefault.baseProductTag" />
    </div>
  </div>
</template>

<script lang="ts">
import {buildOnChange, getEditorValues} from "@azure/api-management-custom-widgets-tools"
import {Values, valuesDefault} from "../../values"

export default {
  data() {
    return {
      productNamePlaceholder: "",
      productDescriptionPlaceholder: "",
      endpoint: "",
      baseProductTag: "",
      valuesDefault,
      onChange: (values: any) => {}
    }
  },

  async mounted(): Promise<void> {
    this.onChange = buildOnChange<Values>()

    const editorData = getEditorValues<Values>()

    this.productNamePlaceholder = editorData.productNamePlaceholder ?? "";
    this.productDescriptionPlaceholder = editorData.productDescriptionPlaceholder ?? "";
    this.endpoint = editorData.endpoint ?? "";
    this.baseProductTag = editorData.baseProductTag ?? "";
  },

  watch: {
    productNamePlaceholder(newValue: string): void {
      this.onChange({productNamePlaceholder: newValue})
    },
    productDescriptionPlaceholder(newValue: string): void {
      this.onChange({productDescriptionPlaceholder: newValue})
    },
    endpoint(newValue: string): void {
      this.onChange({endpoint: newValue})
    },
    baseProductTag(newValue: string): void {
      this.onChange({baseProductTag: newValue})
    },
  }
}
</script>
