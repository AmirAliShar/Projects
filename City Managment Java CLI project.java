import java.util.*;
class ClickCounterThread extends Thread {
    static int count = 0;

    void list_updated(){
        System.out.println("List has been updated !!!!  Thread : " + count++);
    }
    @Override
    public void run() {
        System.out.println("Wait for 1 second Thread has been started....");
        count++;

        try {
            Thread.sleep(1000); // 1 seconds
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        Main2.travel_menu();


    }
}

class Resident {
    String name;
    int experience;
    int price;
    String course_name;
    Resident(){}
    ArrayList<String> ownedItems = new ArrayList<>();
    ArrayList<Integer> item_price_list = new ArrayList<>();
    String person_name, person_address,place_location;
    int  persona_age, ticket;

    void add_item(String item, int price){
        ownedItems.add(item);
        item_price_list.add(price);
//        ownedItems.add("Laptop");ownedItems.add("Bag");ownedItems.add("Book");
//        item_price_list.add(900);item_price_list.add(100);item_price_list.add(590);
    }
    void display_item() {
        System.out.println("═══════════════════════════════════");
        System.out.println("Sr.no  \tItems\t\t\tPrice");
        System.out.println();

        for (int i = 0; i < item_price_list.size(); i++) {
            String item = ownedItems.get(i);
            int price = item_price_list.get(i);
            String formattedSerialNo = String.format("%d", i);
            String formattedPrice = String.format("$%d", price);
            String formattedLine = String.format("%-6s  %-13s %5s", formattedSerialNo, item, formattedPrice);
            System.out.println(formattedLine);
        }

        System.out.println("═══════════════════════════════════");
    }

    public void buyItem(String item) {
        int amount = 0;
        int index = -1;

        for (int i = 0; i < ownedItems.size(); i++) {
            if (ownedItems.get(i).equals(item)) {
                amount = item_price_list.get(i);
                index = i;
                break;
            }
        }

        if (index != -1) {
            ownedItems.remove(index);
            item_price_list.remove(index);
            System.out.println();
            System.out.println("------------------------------------------------------------------");
            System.out.println(item + " " + amount + " purchased and removed from the list.");
            System.out.println("Total amount spent: " + amount);
            System.out.println("Thanks !! for buying " + item);
            System.out.println("------------------------------------------------------------------");
        } else {
            System.out.println("Item not found in the list.");
            System.out.println("------------------------------------------------------------------");
        }
    }

    void add_course(){
        Scanner sc1 = new Scanner(System.in);
        System.out.println("Enter your name : ");
        name = sc1.next();
        System.out.println("Enter your experience in integer: ");
        experience = sc1.nextInt();
        System.out.println("Enter your course name in string: ");
        course_name = sc1.next();
        System.out.println("Enter the course price : ");
        price = sc1.nextInt();
        System.out.println();
    }
    void enrollInCourse() {
        Scanner sc1 = new Scanner(System.in);
        System.out.println("Enter teacher name : ");
        String instructor = sc1.next();
        System.out.println("Enter the course name : ");
        String C_name = sc1.next();
        System.out.println("Enter the price of course : ");
        int C_price = sc1.nextInt();
    }
    void displayCourse(){
        System.out.println(course_name+" \t\t\t\t  "+price+" \t\t\t " +name+" \t\t\t ");
    }
}
class City {
    private String city_name;
    private String location;
    private String Name;
    private int age;

    private ArrayList<Resident> residents;
    public City() {
        residents = new ArrayList<>();
    }
    public void addResident(Resident resident) {
        residents.add(resident);
    }

    public ArrayList<Resident> getResidents() {
        return residents;
    }
    public void add_population() {
        Scanner sc1 = new Scanner(System.in);
        System.out.println("Enter your name : ");
        Name = sc1.next();
        System.out.println("Enter your Address : ");
        location = sc1.next();
        System.out.println("Enter your city name : ");
        city_name = sc1.next();
        System.out.println("Enter your age : ");
        age = sc1.nextInt();
    }
    public void display_population(){
        System.out.println("═══════════════════════════════════════════\n");
        System.out.println("Name    :     "+Name);
        System.out.println("Address :     "+location);
        System.out.println("City    :     " +city_name);
        System.out.println("Age     :     "+age);
        System.out.println("\n═══════════════════════════════════════════\n");
    }

}
class TransportationSystem extends Resident{
    ArrayList<String> places_list = new ArrayList<>();

    ArrayList<Integer> prices_list = new ArrayList<>();
    ArrayList<String> timing_list = new ArrayList<>();
    public void purchaseRailwayTicket(){
        Scanner sc1 = new Scanner(System.in);
        System.out.println("Enter your name : ");
        person_name = sc1.next();
        System.out.println("Enter your address : ");
        person_address= sc1.next();
        System.out.println("Enter your age");
        persona_age = sc1.nextInt();
        System.out.println("Select location : ");
        place_location = sc1.next();

        System.out.print("Enter ticket price : ");
        ticket = sc1.nextInt();

        if( places_list.contains(place_location)){
            System.out.println("\n------------------------------------------------------------------");
            System.out.println("\n *** Thanks for buying ticket  *** \n");
            System.out.println("     Location     : "+place_location);
            System.out.println("     Ticket price : "+ticket);
            System.out.println("\n === Collect your Receipt === ");
            System.out.println("------------------------------------------------------------------");
            System.out.println();

        }
        else {
            System.out.println("\n *** Invalid information ***");
        }
    }
    void add_places(String places, int price, String time){
        places_list.add(places);
        prices_list.add(price);
        timing_list.add(time);

    }
    //2
    void display_places() {
        System.out.println("\n════════════════════════════════════════════════════════════════════════  ");
        System.out.println("\nSerial no       Places List                 Price List         Timing     ");
        System.out.println();

        for (int i = 0; i < places_list.size(); i++) {
            String serialNo = String.format("%-9d", i);
            String places = String.format("%-35s", places_list.get(i));
            String prices = String.format("%-20d", prices_list.get(i));
            String timing = String.format("%-12s", timing_list.get(i));

            System.out.println(serialNo + places + "$"+prices + timing );
        }

        System.out.println("\n════════════════════════════════════════════════════════════════════════  \n");
    }
    public void displayTravelDetails(){
        System.out.println();
        System.out.println();
        System.out.println("═════════════════════════════════════════════════════   \n");
        System.out.println("\n\tName     :     "+person_name);
        System.out.println("\tAddress  :     "+person_address);
        System.out.println("\tAge      :     "+persona_age);
        System.out.println("\tLocation :     "+place_location);
        System.out.println("\tPrice    :     "+ticket);
        System.out.println("\n═════════════════════════════════════════════════════");
        System.out.println();

    }
}

class Main2 {
    static void menu(){

        System.out.println("\nWelcome to the City Management System");
        System.out.println("=====================================");
        System.out.println("      **** Main Menu ****  ");
        System.out.println("   ╔════════════════════════╗   ");
        System.out.println("   ║  1]. Market            ║   ");
        System.out.println("   ║  2]. Training Center   ║   ");
        System.out.println("   ║  3]. Travel            ║   ");
        System.out.println("   ║  4]. Population        ║   ");
        System.out.println("   ║  0]. Exit              ║   ");
        System.out.println("   ╚════════════════════════╝");

        System.out.print("\nEnter your choice: ");


    }
    static void training_center_menu(){
        System.out.println();
        System.out.println("╔═══════════════════════════════════════════════════╗   ");
        System.out.println("║    1]. Enroll Course \t\t\t 2]. Sell Course    ║     ");
        System.out.println("╚═══════════════════════════════════════════════════╝");
        System.out.println();
    }
    static void sub_menu(){
        System.out.println();
        System.out.println("╔═══════════════════════════════════════════════════╗   ");
        System.out.println("║    1]. SELL ITEMS \t\t\t 2]. BUY ITEMS      ║    ");
        System.out.println("╚═══════════════════════════════════════════════════╝");
        System.out.println();

    }
    static void population_menu(){
        System.out.println();
        System.out.println("╔═══════════════════════════════════════════════════╗   ");
        System.out.println("║    1].Add population \t\t\t 2]. Details        ║    ");
        System.out.println("╚═══════════════════════════════════════════════════╝");
        System.out.println();
    }
    static void travel_menu(){
        System.out.println();
        System.out.println("╔═════════════════════════════════════════════════════════════════════════╗   ");
        System.out.println("║    1]. Railway \t\t\t 2]. Add places \t\t\t 3]. Receipt      ║    ");
        System.out.println("╚═════════════════════════════════════════════════════════════════════════╝");
        System.out.println();
    }
    public static void main(String[] args) {

        City city1 = new City();
        Resident resident1 = new Resident();
        city1.addResident(resident1);
        city1.getResidents();



        Main2.menu();
        Main2.call();
    }

    public static void call(){

        TransportationSystem ts1 = new TransportationSystem();

        ts1.add_places("University_of_Sindh_Campus", 200, "10:00AM");
        ts1.add_places("Hyderabad_city_park", 100, "11:59AM");
        ts1.add_places("Kotri_barrage", 500, "03:00PM");

        Resident resident1 = new Resident();
        Resident[] resident2 = new Resident[100];
        int resi_count = 0;
        City city1[] = new City[100];
        int city_count = 0;
        int choice;
        Scanner sc1 = new Scanner(System.in);
        boolean condition = false;
        boolean population_condition = false;
        boolean customer_condition = false;
        boolean resident_condition = false;
        while (true) {
            choice = sc1.nextInt();
            switch (choice) {
                case 1:
                    while (true) {
                        if(condition==false){
                            sub_menu();
                        }
                        else if(condition == true){
                            Main2.menu();
                            call();
                        }

                        int marketChoice = sc1.nextInt();
                        switch (marketChoice) {
                            case 1:
                                resident1.display_item();
                                System.out.print("Enter the item to sell: ");
                                String itemToSell = sc1.next();
                                System.out.print("Enter the price: ");
                                int price = sc1.nextInt();
                                resident1.add_item(itemToSell, price);
                                System.out.println();
                                System.out.println("\n1]. Sell another item");
                                System.out.println("2]. Back to Main-menu\n");
                                int sellChoice = sc1.nextInt();
                                if (sellChoice == 2) {
                                    condition = true;
                                }

                                break;

                            case 2:
                                resident1.display_item();
                                System.out.print("Enter the item to buy: ");
                                String itemToBuy = sc1.next();
                                resident1.buyItem(itemToBuy);

                                System.out.println("\n1]. Buy another item");
                                System.out.println("2]. Back to Main-menu\n");
                                int sellChoice3 = sc1.nextInt();
                                if (sellChoice3 == 2) {
                                    condition = true;


                                }

                                break;

                            default:

                                break;
                        }

                    }

                case 2:
                    while (true) {
                        if(resident_condition==false){
                            training_center_menu();
                        }
                        else if(resident_condition == true){
                            Main2.menu();
                            call();
                        }

                        int residentChoice = sc1.nextInt();
                        switch (residentChoice) {
                            case 1:
                                System.out.println("\n═══════════════════════════════════════════════════════════");
                                System.out.println(" Course \t\t\t Price \t\t\t Instructor");
                                for (int i = 0; i < resi_count; i++) {
                                    resident2[i].displayCourse();

                                }
                                System.out.println("════════════════════════════════════════════════════════════");
                                resident2[resi_count] = new Resident();
                                resident2[resi_count].enrollInCourse();
                                resi_count++;
                                System.out.println("\n *** Thanks for buying course *** ");
                                System.out.println();
                                System.out.println("1]. Purchase another Course : ");
                                System.out.println("2]. Back to Main menu : ");
                                int r_Choice = sc1.nextInt();
                                if (r_Choice == 2) {
                                    resident_condition = true;

                                }

                                break;

                            case 2:
                                resident2[resi_count] = new Resident();
                                resident2[resi_count].add_course();
                                ClickCounterThread thread2 = new ClickCounterThread();
                                thread2.list_updated();
                                resi_count++;

                                System.out.println();
                                System.out.println("1].Add another Course : ");
                                System.out.println("2].Back to Main menu : ");
                                int sellChoice3 = sc1.nextInt();
                                if (sellChoice3 == 2) {
                                    resident_condition = true;

                                }

                                break;

                            default:

                                break;
                        }

                    }

                case 3:
                    while (true) {
                        if(customer_condition==false){
                            ClickCounterThread thread1 = new ClickCounterThread();
                            thread1.start();

                        }
                        else if(customer_condition == true){
                            Main2.menu();
                            call();
                        }

                        int customerChoice = sc1.nextInt();
                        switch (customerChoice) {
                            case 1:
                                ts1.display_places();


                                ts1.purchaseRailwayTicket();

                                System.out.println();
                                System.out.println("1]. Back to Customer-menu");
                                System.out.println("2]. Back to Main-menu");
                                int customerChoice2 = sc1.nextInt();
                                if (customerChoice2 == 2) {
                                    customer_condition = true;
                                }

                                break;

                            case 2:
                                ts1.display_places();

                                System.out.print("Enter the name of place : ");
                                String place = sc1.next();
                                System.out.print("Enter the ticket price : ");
                                int price = sc1.nextInt();
                                System.out.print("Enter the timing of place : ");
                                String timing = sc1.next();
                                ts1.add_places(place, price, timing);
                                System.out.println("\n1]. Back to Customer-menu");
                                System.out.println("2]. Back to Main-menu");
                                int customerChoice3 = sc1.nextInt();
                                if (customerChoice3 == 2) {
                                    customer_condition = true;

                                }
                                break;

                            case 3:

                                ts1.displayTravelDetails();
                                System.out.println("1]. Back to Customer-menu");
                                System.out.println("3]. Back to Main-menu");
                                int customerChoice4 = sc1.nextInt();
                                if (customerChoice4 == 3) {
                                    customer_condition = true;

                                }
                                break;

                            default:

                                break;
                        }

                    }


                case 4:
                    while (true) {
                        if(population_condition==false){
                            population_menu();
                        }
                        else if(population_condition == true){
                            Main2.menu();
                            call();
                        }

                        int poulationChoice = sc1.nextInt();
                        switch (poulationChoice) {
                            case 1:
                                city1[city_count] = new City();
                                city1[city_count].add_population();
                                city_count++;

                                System.out.println();
                                System.out.println("1].Back to population menu : ");
                                System.out.println("2].Back to Main menu : ");
                                int populattionChoice = sc1.nextInt();
                                if (populattionChoice == 2) {
                                    population_condition = true;
                                }

                                break;

                            case 2:

                                for (int i = 0; i < city_count; i++) {
                                    city1[i].display_population();

                                }
                                System.out.println();
                                System.out.println("1].Back to population menu : ");
                                System.out.println("2].Back to Main menu : ");
                                int sellChoice3 = sc1.nextInt();
                                if (sellChoice3 == 2) {
                                    population_condition = true;
                                }

                                break;

                            default:

                                break;
                        }

                    }

                case 0:
                    System.out.println("Exiting the program.....");
                    System.exit(0);


                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

}