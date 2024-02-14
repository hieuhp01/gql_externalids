<h1>Queries</h1>

<strong>ExternalIdCategoryPage:</strong>

<pre>
  <code>
    query externalidcategoryPage {
      externalidcategoryPage {
        id
        name
        nameEn
        created
        lastchange
        changedby {
          id
        }
        createdby {
          id
        }
      }
    }
  </code>
</pre>

<strong>ExternalId:</strong>

<pre>
  <code>
    query externalIds($innerId: UUID = "") {
      externalIds(innerId: $innerId) {
        id
        idType {
          id
          lastchange
          createdby {
            id
          }
        }
        innerId
        outerId
        created
        changedby {
          id
        }
      }
    },
    variables={"innerId"="2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
  </code>
</pre>

<strong>InternalId:</strong>

<pre>
  <code>
    query internalId($outerId: String = "", $typeidId: UUID = "") {
      internalId(outerId: $outerId, typeidId: $typeidId)
    },
    variables={"outerId"="666","typeidId"="d00ec0b6-f27c-497b-8fc8-ddb4e2460717"}
  </code>
</pre>

<strong>ExternalIdById:</strong>

<pre>
  <code>
    query externalidById($id: UUID = "") {
      externalidById(id: $id) {
        id
        idType {
          id
          lastchange
          createdby {
            id
          }
        }
        innerId
        outerId
        created
        changedby {
          id
        }
      }
    },
    variables={"id"="d5d5286d-50d2-4b07-97de-7407c62c21c0"}
  </code>
</pre>

<strong>ExternalIdTypePage:</strong>

<pre>
  <code>
    query externalidtypePage {
      externalidtypePage {
        id
        name
        nameEn
        urlFormat
        category {
          id
        }
        created
        lastchange
        createdby {
          id
        }
        changedby {
          id
        }
      }
    }
  </code>
</pre>

<strong>ExternalidTypebyId:</strong>

<pre>
  <code>
    query externalidtypeById($id: UUID = "") {
      externalidtypeById(id: $id) {
        id
        name
        nameEn
        urlFormat
        category {
          id
        }
        created
        lastchange
        createdby {
          id
        }
        changedby {
          id
        }
      }
    },
    variables={"id"="d00ec0b6-f27c-497b-8fc8-ddb4e2460717"}
  </code>
</pre>

<strong>externalidcategoryInsert:</strong>

<pre>
  <code>
    mutation externalidcategoryInsert($id: UUID!, $name: String!, $nameEn: String!) {
      externalidcategoryInsert(
        externalidcategory: {id: $id, name: $name, nameEn: $nameEn}) {
            id
            msg
            externalidcategory {
                id
                name
            }
        }
    },
    variables={"id": "fc7f95b5-410c-4a26-a4e9-6b0b2a841645", "name": "new name", "nameEn": "new name en"}
  </code>
</pre>

<strong>externalidcategoryUpdate:</strong>

<pre>
  <code>
    mutation ($id: UUID!, $name: String!, $nameEn: String!, $lastchange: DateTime!) {
      externalidcategoryUpdate(
        externalidcategory: {id: $id, name: $name, nameEn: $nameEn,lastchange: $lastchange}) {
            id
            msg
            externalidcategory {
                id
                name
            }
        }
    },
    variables={"id": "0ee3a92d-971f-499a-956f-ca6edb8d6094", "name": "new name", "nameEn": "new name en"}
  </code>
</pre>

<strong>externalidtypeInsert:</strong>

<pre>
  <code>
    mutation ($id: UUID!, $name: String!, $nameEn: String!) {
      externaltypeidInsert(
        externaltypeid: {id: $id, name: $name, nameEn: $nameEn}) {
            id
            msg
            externaltypeid {
                id
                name
                category { id }
            }
        }
    },
    variables={"id": "f6f79926-ac0e-4833-9a38-4272cae33fa6", "name": "new name", "nameEn": "new name en"}
  </code>
</pre>

<strong>externalidtypeUpdate:</strong>

<pre>
  <code>
    mutation ($id: UUID!, $name: String!, $lastchange: DateTime!, $nameEn: String!) {
      externaltypeidUpdate(
        externaltypeid: {id: $id, name: $name, lastchange: $lastchange, nameEn: $nameEn}) {
            id
            msg
            externaltypeid {
                id
                name
            }
        }
    },
    variables={"id": "53697b35-9f67-41e5-abed-04d7d4865cf2", "name": "new name", "nameEn": "new name en"}
  </code>
</pre>

<strong>externalidInsert:</strong>

<pre>
  <code>
    mutation($inner_id: UUID!, $typeid_id: UUID!, $outer_id: String!) { 
        result: externalidInsert(externalid: {innerId: $inner_id, typeidId: $typeid_id, outerId: $outer_id}) { 
            id
            msg
            externalid {
                id
                outerId 
                idType { id }
                lastchange
                created
                changedby { id }             
            }
        }
    }
    , 
    variables={"inner_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "typeid_id": "0c37b3e1-a937-4776-9543-37ae846411de", "outer_id": "777"}
  </code>
</pre>

<strong>externalidUpdate:</strong>

<pre>
  <code>
    mutation ($id: UUID!, $name: String!, $lastchange: DateTime!, $nameEn: String!) {
      externaltypeidUpdate(
        externaltypeid: {id: $id, name: $name, lastchange: $lastchange, nameEn: $nameEn}){
            id
            msg
            externaltypeid {
                id
                name
            }
        }
    },
    variables={"id": "53697b35-9f67-41e5-abed-04d7d4865cf2", "name": "new name", "nameEn": "new name en"}
  </code>
</pre>

<strong>externalidDelete:</strong>

<pre>
  <code>
    mutation($inner_id: UUID!, $typeid_id: UUID!, $outer_id: String!) {
      externalidDelete(
        externalid: {innerId: $inner_id, typeidId: $typeid_id, outerId: $outer_id}) {
                id
                msg
            }
        }
    ,
    variables={"inner_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003", "typeid_id": "d00ec0b6-f27c-497b-8fc8-ddb4e2460717", "outer_id": "666"}
  </code>
</pre>

