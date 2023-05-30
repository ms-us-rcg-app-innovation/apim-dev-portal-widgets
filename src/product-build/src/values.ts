export type Values = {
  productNamePlaceholder: string
  productDescriptionPlaceholder: string
  endpoint: string
  baseProductTag: string
  debugModeEnabled: boolean
}

export const valuesDefault: Readonly<Values> = Object.freeze({
  productNamePlaceholder: "My Product",
  productDescriptionPlaceholder: "This is a custom Product made by the Consumer",
  endpoint: "https://myapim.endpoint/",
  baseProductTag: "base-product",
  debugModeEnabled: false
})
