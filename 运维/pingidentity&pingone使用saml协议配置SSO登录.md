### 一、简介

pingidentity提供有多种协议的SSO，本文档仅为设置saml协议使用。

### 二、步骤

pingidentity的sso功能对接登录上上签，需要以下步骤：

1、上上签为客户提供sp_metadata.xml文件；

2、客户在pingidentity根据sp_metadata.xml文件配置，并生成ldp_metadata.xml文件，发送给上上签，由上上签技术人员在上上签后台进行配置；

3、上上签根据客户提供的ldp_metadata.xml，进行后台配置；

4、双方进行验证配置是否生效；

### 三、配置

##### 1、上上签提供sp_matadata.xml

```xml
<?xml version="1.0"?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" validUntil="2022-06-29T01:32:40Z" cacheDuration="PT604800S" entityID="bestsign_info">
    <md:SPSSODescriptor AuthnRequestsSigned="false" WantAssertionsSigned="false" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
        <md:NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified</md:NameIDFormat>
        <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://ssotest.bestsign.info/users/ignore/saml/sp/consumer" index="1" />
    </md:SPSSODescriptor>
</md:EntityDescriptor>
```

##### 2、登录pingidentity&pingone，配置saml协议相关内容

登录入口网址：https://www.pingidentity.com/en/account/sign-on.html

![img](pingidentity&pingone使用saml协议配置SSO登录.assets/企业微信截图_16590689359385.png)

选择pingone，输入账号，进行人机验证后点击“continue”，进入pingone登录页面，如下

![img](pingidentity&pingone使用saml协议配置SSO登录.assets/企业微信截图_16590689998322.png)

输入账号密码登录即可进入首页，如下

![img](pingidentity&pingone使用saml协议配置SSO登录.assets/企业微信截图_1659069024337.png)

点击上图右侧的sso图标，进入sso配置页面，如下，

![img](pingidentity&pingone使用saml协议配置SSO登录.assets/企业微信截图_1659069073364.png)

按照上图依次点击，点击“Application”旁加号，创建bestsignsso登录的Application，如下

![image-20220729124609933](pingidentity&pingone使用saml协议配置SSO登录.assets/image-20220729124609933.png)

右侧输入“Application”相关基本信息，选择saml application，然后保存即可，进入下个页面，如下

![image-20220729124810809](pingidentity&pingone使用saml协议配置SSO登录.assets/image-20220729124810809.png)

这里选择Manually Enter，配置完成点击save保存，点击刚刚创建的bestsign，进入如下页面，

![image-20220729125108298](pingidentity&pingone使用saml协议配置SSO登录.assets/image-20220729125108298.png)

这里需要在attribute Mappings 处添加email 映射Email Address，如上图配置，配置完成后进入Access页面，如下，

![img](pingidentity&pingone使用saml协议配置SSO登录.assets/企业微信截图_16590695007332.png)



这里需要配置一个group组，点击图中蓝色group，即可进入group页面创建，作用呢，就是此application需要关联一个用户组，之后需要用此application的用户需要加入组里，如上配置即可，之后进入configuration页面，如下图，

![image-20220729125345511](pingidentity&pingone使用saml协议配置SSO登录.assets/image-20220729125345511.png)

点击“Download Metadata”，下载idp_metadata.xml文件，此文件需要提供给上上签，进行上上签侧配置，下载后的文件示例如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<md:EntityDescriptor entityID="https://auth.pingone.asia/7f325c5b-3fd1-4b8a-b725-597fdc7533bd" ID="DUp57Bcq-y4RtkrRLyYj2fYxtqR"
  xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata">
  <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <ds:X509Data>
          <ds:X509Certificate>
            MIIDejCCAmKgAwIBAgIGAYJEzsQ8MA0GCSqGSIb3DQEBCwUAMH4xCzAJBgNVBAYT
            AlVTMRYwFAYDVQQKDA1QaW5nIElkZW50aXR5MRYwFAYDVQQLDA1QaW5nIElkZW50
            aXR5MT8wPQYDVQQDDDZQaW5nT25lIFNTTyBDZXJ0aWZpY2F0ZSBmb3IgQWRtaW5p
            c3RyYXRvcnMgZW52aXJvbm1lbnQwHhcNMjIwNzI4MTIzNjE3WhcNMjMwNzI4MTIz
            NjE3WjB+MQswCQYDVQQGEwJVUzEWMBQGA1UECgwNUGluZyBJZGVudGl0eTEWMBQG
            A1UECwwNUGluZyBJZGVudGl0eTE/MD0GA1UEAww2UGluZ09uZSBTU08gQ2VydGlm
            aWNhdGUgZm9yIEFkbWluaXN0cmF0b3JzIGVudmlyb25tZW50MIIBIjANBgkqhkiG
            9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt+IDdMYx95Crz4UksEtYaMfl9KeR1OggnLWy
            temOjDB6iQkl2FLdw/qupVEccdMgzEJL20WkApHTOrsG5El3UJo5Q92lxWXqU70/
            BULHms5Dx3Ps4bo2+Nd+CEhK/J9/7IT8o/uM39u5wawKMfIdyHDtwEEwXIMcF6ai
            W5XRGof1UjocbYC29ehLRs+TWq3CIMGuUr7yGP98tVHQFeGJVohZml+NkI+6bE8h
            8sAJf/ouH494R0a0g6jCz9LRQO5yXX18pvMNGRNF3V64+96HcArFutSY4xB6Gec2
            /UJICHi6S/FlIF9cz5sfJ/3+IopSZFyXHxPOpa3BgI4fu76uMQIDAQABMA0GCSqG
            SIb3DQEBCwUAA4IBAQBx4aidBottDjsKl9TfO/DQ3A5sCu0aIHom4eiQE+3qfrl3
            U/EyZm71b4ysQ1uNcTd/F5Y+aAgsoiEGaFnv96sC2ZWL3xZWKLRNOGKDmTYvRHpv
            9WE/zWwjtK9ZGTm0yabX70/Dwqmr6FZj4I6qG1wW4suor2byxeOFNHF+ngUTbb36
            6KS0Fm4qtKpYkPD9oIJhGbQjcoeztoSyIgkdBzn/9Nz8jQHB/K+gIbFb6crrm0K9
            +x9URER6UHFBj1yJWgln6AksJehb+1K7AXvzGDGn1RPKJH2RldN+pPq5HcXSc3wM
            85K8FFxuFxD7QK3QRh4MiLTlOab+LI6pDwPgMlnR
          </ds:X509Certificate>
        </ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>
    <md:SingleLogoutService Location="https://auth.pingone.asia/7f325c5b-3fd1-4b8a-b725-597fdc7533bd/saml20/idp/slo" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"/>
    <md:SingleLogoutService Location="https://auth.pingone.asia/7f325c5b-3fd1-4b8a-b725-597fdc7533bd/saml20/idp/slo" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"/>
    <md:SingleSignOnService Location="https://auth.pingone.asia/7f325c5b-3fd1-4b8a-b725-597fdc7533bd/saml20/idp/sso" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"/>
    <md:SingleSignOnService Location="https://auth.pingone.asia/7f325c5b-3fd1-4b8a-b725-597fdc7533bd/saml20/idp/sso" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.locale"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.mobilePhone"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.nickname"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.identityProvider.type"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.identityProvider.id"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.enabled"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.photo.href"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.email"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.lastSignOn.remoteIp"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.lastSignOn.at"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.preferredLanguage"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.population.id"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.verifyStatus"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.username"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.memberOfGroupIDs"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.address.region"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.address.streetAddress"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.address.locality"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.address.postalCode"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.address.countryCode"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.mfaEnabled"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.externalId"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.title"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.account.unlockAt"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.account.lockedAt"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.account.canAuthenticate"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.account.secondsUntilUnlock"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.account.status"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.type"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.name.family"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.name.honorificPrefix"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.name.formatted"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.name.middle"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.name.honorificSuffix"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.name.given"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.lifecycle.status"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.timezone"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.accountId"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.createdAt"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.id"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.memberOfGroupNames"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.primaryPhone"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
    <saml:Attribute NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic" Name="user.updatedAt"
      xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"/>
  </md:IDPSSODescriptor>
</md:EntityDescriptor>
```



##### 3、上上签后台配置

上上签拿到用户配置后，打开如下，解释下上上签能用到那些：红色框中是x509公钥，需要配置在上上签后台，下面红色框是location，一些配置地址，也需要配置在上上签后台。

![image-20220729125627534](pingidentity&pingone使用saml协议配置SSO登录.assets/image-20220729125627534.png)

进入上上签后台，配置如下，

![image-20220729130011673](pingidentity&pingone使用saml协议配置SSO登录.assets/image-20220729130011673.png)
描述下配置如何选择：

1、sso协议：选saml；

2、跳转登录也地址：https://ssotest.bestsign.info/users/ignore/saml/idp/ssotest，需要注意，域名是为客户申请的二级域名，末尾的ssotest要替换为客户的二级域名的二级名；

3、退出登录：后续功能出来再配置；

4、类型：写当天配置时间；

5、必须使用企业内部邮箱作为账号：勾选只能用邮箱；

6、SingleSignOnService：跳转登录地址，如上图配置；

7、第三方用户信息：推荐email，跟企业相关，也要看企业的配置，推荐email；

8、comparison：显式写EXACT，默认现在不生效；

9、登录策略：选X509，当然这个跟客户的配置有关；

10、私钥信息：这个应该是x509公钥，有的客户的idp_metadata.xml文件有公私钥，注意此处要用公钥；