import { faker } from "@faker-js/faker";
import { TrieWrapper } from "./tries";


for (let i = 100; i < 2000; i+= 100){
    const words = Array.from({length: i},() => faker.datatype.string(i));
    const trie = new TrieWrapper(words)
    const thingsToSearch = Array.from({length: 100000},() => faker.datatype.string(i)); 
    let startTime = new Date()
    for (const word in thingsToSearch){
        trie.doesWordExist(word)
    }
    const WordCheckTime = new Date().getTime() - startTime.getTime()
    console.log(`For ${i} words (${i} characters) checkin took ${WordCheckTime} ms (100k lookups).`)
}