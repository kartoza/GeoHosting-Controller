import {Package} from "../redux/reducers/productsSlice";

export const isEmpty = value =>
  value === undefined ||
  value === null ||
  (typeof value === "object" && Object.keys(value).length === 0) ||
  (typeof value === "string" && value.trim().length === 0);

export const formatPrice = (price: string, currency = 'USD') => {
    const locale = navigator.language;
    let formattedPrice = new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(parseFloat(price));

    if (formattedPrice.endsWith('.00')) {
      formattedPrice = formattedPrice.slice(0, -3);
    }

    return formattedPrice;
  };

export const packageName = (pkg: Package) => {
  if (pkg.name.toLowerCase().includes('small')) {
    return 'Basic';
  } else if (pkg.name.toLowerCase().includes('medium')) {
    return 'Advanced';
  } else {
    return 'Gold';
  }
};
