export const startStripeCheckout = async (
  productType: string,
  extraData: Record<string, unknown> = {}
) => {
  const token = localStorage.getItem("token");

  if (!token) {
    window.location.href = "/register";
    return;
  }

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/payments/create-checkout-session`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        product_type: productType,
        ...extraData,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Unable to create checkout session");
  }

  if (data.checkout_url) {
    window.location.href = data.checkout_url;
  }
};