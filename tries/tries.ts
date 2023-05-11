
// Node of the trie datastructure
export class TrieNode {
    private next: Map<string, TrieNode> = new Map<string, TrieNode>()
    isTerminal = false

    registerChild(character: string): TrieNode{
        const existingNext = this.next.get(character)
        if (!existingNext){
            const newNext = new TrieNode();
            this.next.set(character, newNext)
            return newNext
        }
        return existingNext
    }

    isInChildren(word: string): boolean{
        if (word.length === 0){
            return this.isTerminal
        }
        const next = this.next.get(word[0])
        if (!next){
            return false
        }
        return next.isInChildren(word.slice(1))
    }

    getNestedNext(prefix: string): TrieNode | null{
        if (prefix.length === 0){
            return this
        }
        const next = this.next.get(prefix[0])
        if (!next){
            return null
        }
        return next.getNestedNext(prefix.slice(1))
    }

    getSuffixes(): string[]{
        let output:string [] = []
        if (this.isTerminal){
            output.push('')
        }
        for (const char of Array.from(this.next.keys())){
            const next = this.next.get(char)
            if (!next){
                continue
            }
            output = output.concat(next.getSuffixes().map((suffix) => char + suffix))
        }
        return output
    }
}

export class TrieWrapper{
    private root: TrieNode
    constructor(words: string[]){
        this.buildTrie(words)
    }

    private buildTrie(words: string[]){
        this.root = new TrieNode()
        for (const word of words){
            let node = this.root
            for (let i = 0; i < word.length; i++){
                const char = word.charAt(i)
                node = node.registerChild(char)
            }
            node.isTerminal = true
        }
    }

    doesWordExist(word: string){
        return this.root.isInChildren(word)
    }

    getWordsStartingWith(prefix: string): string[]{
        const startNode = this.root.getNestedNext(prefix)
        if (!startNode){
            return []
        }
        const output = startNode.getSuffixes()
        return output.map((suffix) => prefix+suffix)
    }
}
