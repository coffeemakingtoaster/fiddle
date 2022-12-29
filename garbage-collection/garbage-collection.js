const fs = require('fs')
const style = +process.argv[2] || 0; // Run with GC by default
const endTime = Date.now() + ( +process.argv[3] || 1000) // Run for 1 second by default
let resultsHaveBeenCollected = false

function generateSampleObject() {
  // Object containing 2 booleans, 2 strings, 2 numbers, 2 arrays, 2 Objects
  return {
    prop1: true,
    prop2: false,
    prop3: "string",
    prop4: "long string",
    prop5: 1.24,
    prop6: 3.14,
    prop7: ["abc", "def"],
    prop8: [1, 2],
    prop9: { a: "a", b: "b" },
    prop10: { a: "b", b: "a" },
  };
}

/**
 * @description Copy to new object by assigning values 
 */
function copyViaAssignment(oldObj, newValues) {
  oldObj.prop1 = newValues.prop1;
  oldObj.prop2 = newValues.prop2;
  oldObj.prop3 = newValues.prop3;
  oldObj.prop4 = newValues.prop4;
  oldObj.prop5 = newValues.prop5;
  oldObj.prop6 = newValues.prop6;
  oldObj.prop7 = newValues.prop7;
  oldObj.prop8 = newValues.prop8;
  oldObj.prop9 = newValues.prop9;
  oldObj.prop10 = newValues.prop10;
}

/**
 * @description Simplistic Objectstore
 */
class ObjectStore {
  constructor(factory) {
    this.factory = factory;
    this.pool = new Array();
    this.len = 0;
  }

  /**
   * @description Return poolvalue or return newly generated Object
   */
  get() {
    if (this.len > 0) {
      const out = this.pool[this.len - 1];
      this.len--;
      return out;
    }
    return this.factory();
  }

  // Take in items and place into pool
  releaseBulk(items) {
    for (let j = 0; j < items.length; ++this.len, ++j) {
      this.pool[this.len] = items[j];
    }
  }
}

const store = new ObjectStore(generateSampleObject);

function copyViaSomething(newObj) {
  // Copy via spreading
  if (style === 0) {
    return { ...newObj };
  }
  // Get Prop from store
  const nextObj = store.get();
  // Overwrite properties of nextProp with prop
  copyViaAssignment(nextObj, newObj)
  return nextObj;
}

const temporaryMemory = [];
/**
 * @description Formatted Result output
 */
function result() {
  const now = Date.now();
const filepath = `raw_logs/${style === 0? 'garbage-collection.json': 'objectPooling.jsoni'}`
  //console.log(`Results:\n\tDuration in ms: ${now-start}\n\tTotal objects created: ${totalCount}\n\tObjects created per ms: ${totalCount / (now-start)}`)
  let data = []
	if (fs.existsSync(filepath)){
data =  JSON.parse(fs.readFileSync(filepath))
	}
  data.push({
	duration: now-start,
	totalCount: totalCount,
	  createdPerMs: totalCount/(now-start)
  })
  // Sort by duration
  data.sort((a,b) => a.duration - b.duration)
  fs.writeFileSync(filepath, JSON.stringify(data))
}

/**
 * @description Handle cleanup of objects by either removing all references (GC) or readding them to the ObjectStore pool
 */
function collect() {
  // Release back into ObjectStore
  if (style === 1) {
    store.releaseBulk(temporaryMemory);
  }
  // Clean temporary memory => If no more references are being held (i.e. they have not been copied into ObjectStore) the GC will clean them up
  temporaryMemory.length = 0;
  // If time exceeded runtime => end run
  if (Date.now() >= endTime) {
      resultsHaveBeenCollected = true
    
  }
}

let totalCount = 0;
let start = Date.now();
function main() {
  // amount of objects to generate
  const howMuch = 100;
  const howLong = 100; // time in ms
  const props = generateSampleObject();
  let collectTime = Date.now() + howLong;

  while (!resultsHaveBeenCollected) {
    // Insert elemtents into array
    for (let i = 0; i < howMuch; ++i) {
      temporaryMemory.push(copyViaSomething(props));
    }
    totalCount += howMuch;
    if (collectTime < Date.now()) {
      collectTime += howLong;
      collect();
    }
  }
}


main();
result()

