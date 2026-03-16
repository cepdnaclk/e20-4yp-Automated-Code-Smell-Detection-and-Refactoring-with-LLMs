public class OrderProcessor {

    public void processOrder(String customerType, int quantity, double pricePerItem, boolean isInternational) {

        double totalPrice = 0.0;
        double discount = 0.0;
        double tax = 0.0;
        double shippingCost = 0.0;

        // Step 1: Calculate base price
        totalPrice = quantity * pricePerItem;

        // Step 2: Apply discount based on customer type
        if (customerType.equals("REGULAR")) {
            if (quantity > 50) {
                discount = totalPrice * 0.05;
            } else if (quantity > 100) {
                discount = totalPrice * 0.10;
            }
        } else if (customerType.equals("PREMIUM")) {
            if (quantity > 50) {
                discount = totalPrice * 0.10;
            } else if (quantity > 100) {
                discount = totalPrice * 0.15;
            } else {
                discount = totalPrice * 0.05;
            }
        } else if (customerType.equals("VIP")) {
            discount = totalPrice * 0.20;
        }

        totalPrice = totalPrice - discount;

        // Step 3: Calculate tax
        if (isInternational) {
            tax = totalPrice * 0.18;
        } else {
            tax = totalPrice * 0.12;
        }

        totalPrice = totalPrice + tax;

        // Step 4: Calculate shipping cost
        if (isInternational) {
            if (quantity < 10) {
                shippingCost = 50.0;
            } else if (quantity < 50) {
                shippingCost = 30.0;
            } else {
                shippingCost = 10.0;
            }
        } else {
            if (quantity < 10) {
                shippingCost = 20.0;
            } else if (quantity < 50) {
                shippingCost = 10.0;
            } else {
                shippingCost = 0.0;
            }
        }

        totalPrice = totalPrice + shippingCost;

        // Step 5: Print invoice details
        System.out.println("------ INVOICE ------");
        System.out.println("Customer Type: " + customerType);
        System.out.println("Quantity: " + quantity);
        System.out.println("Price per Item: " + pricePerItem);
        System.out.println("Discount Applied: " + discount);
        System.out.println("Tax Applied: " + tax);
        System.out.println("Shipping Cost: " + shippingCost);
        System.out.println("Final Amount: " + totalPrice);
        System.out.println("---------------------");

        // Step 6: Store order (simulated)
        if (totalPrice > 1000) {
            System.out.println("Order stored as HIGH VALUE order.");
        } else {
            System.out.println("Order stored as REGULAR order.");
        }

        // Step 7: Send notifications (simulated)
        if (customerType.equals("VIP")) {
            System.out.println("Sending priority notification to VIP customer.");
        } else {
            System.out.println("Sending standard notification to customer.");
        }
    }
}
