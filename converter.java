recordDetails, Array
total, Integer
noOfRecordsPerPage, Integer
currentPageOffset, Integer
message, Null
accountId, String
accountBranch, String
accountType, String
spreadType, String
spreadTypeIdentifier, String
currencyPocketType, String
CCy1Value, String
cCy2Value, String
instrument, String
spreadHierarchyType, String
spreadCategory, String
spreadMethod, String
tenor, String
inclusiveLowerLimit, Integer
maxLimit, Boolean
spread, String
-------------------------------

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.reflect.TypeToken;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.*;

public class JsonToCsvConverter {
    public static void main(String[] args) {
        String inputFilePath = "path_to_your_json_file.json";
        String outputFilePath = "output.csv";

        try (FileReader reader = new FileReader(inputFilePath)) {
            JsonObject jsonObject = JsonParser.parseReader(reader).getAsJsonObject();
            List<LinkedHashMap<String, String>> flatData = new ArrayList<>();
            flattenJson(jsonObject, new LinkedHashMap<>(), flatData);

            writeCsv(flatData, outputFilePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void flattenJson(JsonObject jsonObject, LinkedHashMap<String, String> currentMap, List<LinkedHashMap<String, String>> flatData) {
        JsonArray accountDetailsArray = jsonObject.getAsJsonArray("accountDetails");
        if (accountDetailsArray != null) {
            for (int i = 0; i < accountDetailsArray.size(); i++) {
                JsonObject accountDetails = accountDetailsArray.get(i).getAsJsonObject();
                LinkedHashMap<String, String> accountMap = new LinkedHashMap<>(currentMap);
                accountMap.put("accountId", accountDetails.get("accountId").getAsString());
                accountMap.put("accountBranch", accountDetails.get("accountBranch").getAsString());
                accountMap.put("accountType", accountDetails.get("accountType").getAsString());

                JsonArray spreadTypesArray = accountDetails.getAsJsonArray("spreadTypes");
                if (spreadTypesArray != null) {
                    for (int j = 0; j < spreadTypesArray.size(); j++) {
                        JsonObject spreadType = spreadTypesArray.get(j).getAsJsonObject();
                        LinkedHashMap<String, String> spreadTypeMap = new LinkedHashMap<>(accountMap);
                        spreadTypeMap.put("spreadType", spreadType.get("spreadType").getAsString());
                        spreadTypeMap.put("spreadTypeIdentifier", spreadType.get("spreadTypeIdentifier").getAsString());

                        JsonArray currencyPocketsArray = spreadType.getAsJsonArray("currencyPockets");
                        if (currencyPocketsArray != null) {
                            for (int k = 0; k < currencyPocketsArray.size(); k++) {
                                JsonObject currencyPocket = currencyPocketsArray.get(k).getAsJsonObject();
                                LinkedHashMap<String, String> currencyPocketMap = new LinkedHashMap<>(spreadTypeMap);
                                currencyPocketMap.put("currencyPocketType", currencyPocket.get("currencyPocketType").getAsString());
                                currencyPocketMap.put("CCy1Value", currencyPocket.get("CCy1Value").getAsString());
                                currencyPocketMap.put("cCy2Value", currencyPocket.get("cCy2Value").getAsString());

                                JsonArray instrumentsArray = currencyPocket.getAsJsonArray("instruments");
                                if (instrumentsArray != null) {
                                    for (int l = 0; l < instrumentsArray.size(); l++) {
                                        JsonObject instrument = instrumentsArray.get(l).getAsJsonObject();
                                        LinkedHashMap<String, String> instrumentMap = new LinkedHashMap<>(currencyPocketMap);
                                        instrumentMap.put("instrument", instrument.get("instrument").getAsString());

                                        JsonArray spreadHierarchyTypesArray = instrument.getAsJsonArray("spreadHierarchyTypes");
                                        if (spreadHierarchyTypesArray != null) {
                                            for (int m = 0; m < spreadHierarchyTypesArray.size(); m++) {
                                                JsonObject spreadHierarchyType = spreadHierarchyTypesArray.get(m).getAsJsonObject();
                                                LinkedHashMap<String, String> spreadHierarchyTypeMap = new LinkedHashMap<>(instrumentMap);
                                                spreadHierarchyTypeMap.put("spreadHierarchyType", spreadHierarchyType.get("spreadHierarchyType").getAsString());
                                                spreadHierarchyTypeMap.put("spreadCategory", spreadHierarchyType.get("spreadCategory").getAsString());
                                                spreadHierarchyTypeMap.put("spreadMethod", spreadHierarchyType.get("spreadMethod").getAsString());

                                                JsonArray tenorsArray = spreadHierarchyType.getAsJsonArray("tenors");
                                                if (tenorsArray != null) {
                                                    for (int n = 0; n < tenorsArray.size(); n++) {
                                                        JsonObject tenor = tenorsArray.get(n).getAsJsonObject();
                                                        LinkedHashMap<String, String> tenorMap = new LinkedHashMap<>(spreadHierarchyTypeMap);
                                                        tenorMap.put("tenor", tenor.get("tenor").getAsString());

                                                        JsonArray limitsArray = tenor.getAsJsonArray("limits");
                                                        if (limitsArray != null) {
                                                            for (int o = 0; o < limitsArray.size(); o++) {
                                                                JsonObject limit = limitsArray.get(o).getAsJsonObject();
                                                                LinkedHashMap<String, String> limitMap = new LinkedHashMap<>(tenorMap);
                                                                limitMap.put("inclusiveLowerLimit", limit.get("inclusiveLowerLimit").getAsString());
                                                                limitMap.put("maxLimit", limit.get("maxLimit").getAsString());
                                                                limitMap.put("spread", tenor.get("spread").getAsString());

                                                                // Add the flattened data to the list
                                                                flatData.add(limitMap);
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    private static void writeCsv(List<LinkedHashMap<String, String>> flatData, String filePath) {
        if (flatData.isEmpty()) {
            return;
        }

        try (FileWriter writer = new FileWriter(filePath)) {
            // Write CSV header
            Set<String> headers = flatData.get(0).keySet();
            writer.append(String.join(",", headers));
            writer.append("\n");

            // Write CSV data
            for (LinkedHashMap<String, String> row : flatData) {
                for (String header : headers) {
                    writer.append(row.getOrDefault(header, ""));
                    writer.append(",");
                }
                writer.append("\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
