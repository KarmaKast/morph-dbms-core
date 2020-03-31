import * as Structs from "./structs";
import * as fs from "fs";
import * as path from "path";

export async function initDatabase(
  dataBasePath: string,
  mode: "init" | "reset" = "init"
): Promise<void> {
  function init(): void {
    fs.mkdirSync(dataBasePath, { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Entities"), { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Collections"), { recursive: true });
    fs.mkdirSync(path.join(dataBasePath, "Relations"), { recursive: true });
  }
  switch (mode) {
    case "reset":
      // remove the database folder completely
      if (fs.existsSync(dataBasePath)) {
        fs.rmdirSync(dataBasePath, { recursive: true });
      }
      init();
      return new Promise((resolve, reject) => {
        console.log("reset done");
        resolve();
      });

      break;
    case "init":
      // check database folder integrity
      if (!fs.existsSync(dataBasePath)) {
        init();
      }
      break;
  }
}

export function writeEntity(
  entity: Structs.Entity,
  dataBasePath: string
): void {
  fs.writeFileSync(
    path.resolve(path.join(dataBasePath, "Entities", entity.ID + ".entity")),
    JSON.stringify(entity),
    { flag: "w+" }
  );
}

export function writeCollection(
  collection: Structs.Collection,
  dataBasePath: string
): void {
  for (const entityID in collection.Entities) {
    writeEntity(collection.Entities[entityID], dataBasePath);
  }
  fs.writeFile(
    path.resolve(
      path.join(dataBasePath, "Collections", collection.ID + ".collection")
    ),
    JSON.stringify(collection),
    { flag: "w+" },
    (err) => {
      if (err) throw err;
      console.log("The file has been saved!");
    }
  );
}
